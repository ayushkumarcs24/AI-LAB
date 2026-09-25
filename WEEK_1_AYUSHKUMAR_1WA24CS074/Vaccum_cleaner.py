class VacuumCleanerAgent:
    def __init__(self, location='A', status_A='Dirty', status_B='Dirty'):
        self.location = location  # 'A' or 'B'
        self.environment = {'A': status_A, 'B': status_B} # 'Dirty' or 'Clean'

    def perceive(self):
        return self.location, self.environment[self.location]

    def act(self, precept):
        current_location, current_status = precept

        print(f"Agent at {current_location}, status: {current_status}")

        if current_status == 'Dirty':
            print(f"Action: Clean at {current_location}")
            self.environment[current_location] = 'Clean'
            return 'Clean'
        elif current_location == 'A':
            print("Action: Move Right to B")
            self.location = 'B'
            return 'Move Right'
        elif current_location == 'B':
            print("Action: Move Left to A")
            self.location = 'A'
            return 'Move Left'

def run_vacuum_cleaner_simulation(steps=10, initial_location='A', initial_status_A='Dirty', initial_status_B='Dirty'):
    agent = VacuumCleanerAgent(initial_location, initial_status_A, initial_status_B)
    print("AYUSH KUMAR USN_ 1WA24CS074")
    print("--- Vacuum Cleaner Simplex Reflex Agent Simulation ---")
    print(f"Initial State: Location={agent.location}, Room A={agent.environment['A']}, Room B={agent.environment['B']}")

    for i in range(steps):
        print(f"\nStep {i+1}:")
        precept = agent.perceive()
        agent.act(precept)
        print(f"Current State: Location={agent.location}, Room A={agent.environment['A']}, Room B={agent.environment['B']}")

        if agent.environment['A'] == 'Clean' and agent.environment['B'] == 'Clean':
            print("Both rooms are clean. Simulation can end early.")
            break

    print("\n--- Simulation End ---")
run_vacuum_cleaner_simulation(steps=10, initial_location='A', initial_status_A='Dirty', initial_status_B='Dirty')