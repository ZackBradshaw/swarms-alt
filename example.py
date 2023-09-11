from swarms import Worker

node = Worker(
    openai_api_key="",
    ai_name="Optimus Prime",

)

task = "What were the winning boston marathon times for the past 5 years (ending in 2022)? Generate a table of the year, name, country of origin, and times."
response = node.run(task)
print(response)