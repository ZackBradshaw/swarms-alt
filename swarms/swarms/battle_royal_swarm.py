"""

Battle royal swarm where agents compete to be the first to answer a question. or the best answer.
Look to fornight game

teams of 1, 3 or 4 that equates to 100 total agents


Communication is proximal and based on proximity
Clashes with adversial agents not in team.

Teams of 3 agents would fight each other and then move on while other agents are clashing with eachother as well.

Agents can be in multiple teams
Agents can be in multiple teams and be adversial to each other
Agents can be in multiple teams and be adversial to each other and be in multiple teams
"""
import random
from swarms.workers.worker import Worker


class BattleRoyalSwarm:
    def __init__(self, human_evaluator=None):
        self.workers = [Worker() for _ in range(100)]
        self.teams = self.form_teams()
        self.human_evaluator = human_evaluator

    def form_teams(self):
        teams = []
        unassigned_workers = self.workers.copy()
        while unassigned_workers:
            size = random.choice([1, 3, 4])
            team = [
                unassigned_workers.pop()
                for _ in range(min(size, len(unassigned_workers)))
            ]
            for worker in team:
                worker.teams.append(team)
            teams.append(team)
        return teams

    def broadcast_question(self, question: str):
        responses = {}
        for worker in self.workers:
            response = worker.run(question)
            responses[worker.id] = response

        # Check for clashes and handle them
        for i, worker1 in enumerate(self.workers):
            for j, worker2 in enumerate(self.workers):
                if (
                    i != j
                    and worker1.is_within_proximity(worker2)
                    and set(worker1.teams) != set(worker2.teams)
                ):
                    winner, loser = self.clash(worker1, worker2, question)
                    print(f"Worker {winner.id} won over Worker {loser.id}")

    def communicate(self, sender: Worker, reciever: Worker, message: str):
        if sender.is_within_proximity(reciever) or any(
            team in sender.teams for team in reciever.teams
        ):
            pass

    def clash(self, worker1: Worker, worker2: Worker, question: str):
        solution1 = worker1.run(question)
        solution2 = worker2.run(question)
        score1, score2 = self.human_evaluator(solution1, solution2)
        if score1 > score2:
            return worker1, worker2
        return worker2, worker1
