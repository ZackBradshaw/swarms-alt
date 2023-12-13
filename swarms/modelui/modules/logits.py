import torch
from transformers import is_torch_xpu_available

from swarms.modelui.modules import sampler_hijack, shared
from swarms.modelui.modules.logging_colors import logger
from swarms.modelui.modules.text_generation import generate_reply

global_scores = None


def get_next_logits(prompt, state, use_samplers, previous):
    if shared.model is None:
        logger.error("No model is loaded! Select one in the Model tab.")
        return "Error: No model is loaded1 Select one in the Model tab.", previous

    is_non_hf_exllamav2 = shared.model.__class__.__name__ == "Exllamav2Model"
    is_non_hf_exllamav1 = shared.model.__class__.__name__ == "ExllamaModel"
    is_non_hf_llamacpp = shared.model.__class__.__name__ == "LlamaCppModel"

    if use_samplers:
        if any([is_non_hf_exllamav2, is_non_hf_exllamav1, is_non_hf_llamacpp]):
            logger.error("Sampler hijacking is not supported non-Huggingface loaders.")
            # sampling is all done in c for exllama, so it is really hard to hijack
            # it should be possible to hijack llamacpp sampler by hijacking all their sampling methods,
            # but it is not implemented yet
            return (
                'Error: Sampler hijacking is not supported non-Huggingface loaders. Please disable the "Use samplers" option.',
                previous,
            )

        state["max_new_tokens"] = 1
        state["auto_max_new_tokens"] = False
        for _ in generate_reply(prompt, state):
            pass

        scores = sampler_hijack.global_scores[-1]
    else:
        if is_non_hf_exllamav2 or is_non_hf_exllamav1:
            if is_torch_xpu_available():
                tokens = shared.tokenizer.encode(prompt).to("xpu:0")
            else:
                tokens = shared.tokenizer.encode(prompt).cuda()
            scores = shared.model.get_logits(tokens)[-1][-1]
        elif is_non_hf_llamacpp:
            tokens = shared.tokenizer.encode(prompt)
            scores = shared.model.get_logits(tokens)[-1][-1]
        else:
            if is_torch_xpu_available():
                tokens = shared.tokenizer.encode(prompt, return_tensors="pt").to(
                    "xpu:0"
                )
            else:
                tokens = shared.tokenizer.encode(prompt, return_tensors="pt").cuda()
            output = shared.model(input_ids=tokens)
            scores = output["logits"][-1][-1]

    probs = torch.softmax(scores, dim=-1, dtype=torch.float)
    topk_values, topk_indices = torch.topk(probs, k=50, largest=True, sorted=True)
    topk_values = [f"{float(i):.5f}" for i in topk_values]
    if is_non_hf_exllamav1 or is_non_hf_llamacpp:
        topk_indices = [i.expand((1, 1)) for i in topk_indices]

    tokens = [shared.tokenizer.decode(i) for i in topk_indices]
    output = ""
    for row in list(zip(topk_values, tokens)):
        output += f"{row[0]}  -  {repr(row[1])}\n"

    return output, previous