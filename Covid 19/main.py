from experta import *
import tkinter as tk
from tkinter import messagebox

levels_with_questions = [
    {
        "level": 1,
        "level_title": "General Symptoms",
        "questions": [
            {"question": "Do you have a fever?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "High": 3}},
            {"question": "Do you have a dry cough?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Do you feel tired?", "options": {"No": 0, "Sometimes": 1, "Often": 2, "Always": 3}},
            # {"question": "Do you have chills?", "options": {"No": 0, "Rarely": 1, "Often": 2, "Always": 3}},
        ]
    },
    {
        "level": 2,
        "level_title": "Breathing and Chest Symptoms",
        "questions": [
            {"question": "Do you have difficulty breathing?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Do you feel chest pain?", "options": {"No": 0, "Rare": 1, "Often": 2, "Severe": 3}},
            # {"question": "Is your voice hoarse?", "options": {"No": 0, "Slightly": 1, "Noticeable": 2, "Very Hoarse": 3}},
            {"question": "Do you have a sore throat?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
        ]
    },
    {
        "level": 3,
        "level_title": "Sensory Symptoms",
        "questions": [
            {"question": "Do you experience loss of smell?", "options": {"No": 0, "Slight": 1, "Moderate": 2, "Complete": 3}},
            # {"question": "Do you experience loss of taste?", "options": {"No": 0, "Slight": 1, "Moderate": 2, "Complete": 3}},
            {"question": "Do you suffer from nasal congestion?", "options": {"No": 0, "Rare": 1, "Often": 2, "Severe": 3}},
            {"question": "Are you sneezing frequently?", "options": {"No": 0, "Rarely": 1, "Often": 2, "Always": 3}},
        ]
    },
    {
        "level": 4,
        "level_title": "Pain and Aches Symptoms",
        "questions": [
            {"question": "Do you feel headaches?", "options": {"No": 0, "Rare": 1, "Often": 2, "Severe": 3}},
            {"question": "Do you feel muscle pain?", "options": {"No": 0, "Rare": 1, "Often": 2, "Severe": 3}},
            # {"question": "Are your joints aching?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Are you experiencing body aches?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
        ]
    },
    {
        "level": 5,
        "level_title": "Digestive Symptoms",
        "questions": [
            {"question": "Do you feel nausea?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
            # {"question": "Do you have diarrhea?", "options": {"No": 0, "Mild": 1, "Frequent": 2, "Severe": 3}},
            {"question": "Do you feel stomach pain?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Do you feel like vomiting?", "options": {"No": 0, "Sometimes": 1, "Often": 2, "Always": 3}},
        ]
    },
    {
        "level": 6,
        "level_title": "Mental Symptoms",
        "questions": [
            {"question": "Are you feeling dizzy?", "options": {"No": 0, "Sometimes": 1, "Often": 2, "Always": 3}},
            # {"question": "Do you have confusion or brain fog?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Do you feel anxiety?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Do you have trouble sleeping?", "options": {"No": 0, "Sometimes": 1, "Often": 2, "Always": 3}},
        ]
    },
    {
        "level": 7,
        "level_title": "Pre-existing Conditions",
        "questions": [
            {"question": "Do you have pre-existing heart disease?", "options": {"No": 0, "Mild": 1, "Managed": 2, "Severe": 3}},
            {"question": "Do you have diabetes?", "options": {"No": 0, "Controlled": 1, "Uncontrolled": 2, "Severe": 3}},
            {"question": "Do you have hypertension?", "options": {"No": 0, "Controlled": 1, "Uncontrolled": 2, "Severe": 3}},
            # {"question": "Do you have any autoimmune disease?", "options": {"No": 0, "Mild": 1, "Moderate": 2, "Severe": 3}},
        ]
    },
    {
        "level": 8,
        "level_title": "Risk Factors",
        "questions": [
            {"question": "Are you above 60 years old?", "options": {"No": 0, "Slightly": 1, "60–75": 2, "75+": 3}},
            {"question": "Do you live with someone who tested positive?", "options": {"No": 0, "Contact > 7 days": 1, "Recent contact": 2, "Currently positive": 3}},
            # {"question": "Do you work in a healthcare setting?", "options": {"No": 0, "Occasionally": 1, "Often": 2, "Always": 3}},
            {"question": "Are you vaccinated?", "options": {"Yes (2 doses)": 0, "Yes (1 dose)": 1, "Unvaccinated": 2, "Decline to say": 3}},
        ]
    }
]


class CovidExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.risk_result = None

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="diagnose")

    # Low risk: total_score ≤ 32  (about one-third of max 96)
    @Rule(Fact(action='diagnose'),
          Fact(total_score=MATCH.s & P(lambda s: s <= 32)))
    def low_risk(self, s):
        self.risk_result = "Low Risk"

    # Moderate risk: 33–64
    @Rule(Fact(action='diagnose'),
          Fact(total_score=MATCH.s & P(lambda s: 33 <= s <= 64)))
    def moderate_risk(self, s):
        self.risk_result = "Moderate Risk"

    # High risk: >64
    @Rule(Fact(action='diagnose'),
          Fact(total_score=MATCH.s & P(lambda s: s > 64)))
    def high_risk(self, s):
        self.risk_result = "High Risk"


class CovidExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.risk_result = None

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="diagnose")

    @Rule(Fact(action='diagnose'),
          Fact(total_score=MATCH.s & P(lambda s: s <= 32)))
    def low_risk(self, s):
        self.risk_result = "Low Risk"

    @Rule(Fact(action='diagnose'),
          Fact(total_score=MATCH.s & P(lambda s: 33 <= s <= 64)))
    def moderate_risk(self, s):
        self.risk_result = "Moderate Risk"

    @Rule(Fact(action='diagnose'),
          Fact(total_score=MATCH.s & P(lambda s: s > 64)))
    def high_risk(self, s):
        self.risk_result = "High Risk"


class CovidDiagnosisApp:
    def __init__(self, root):
        self.root = root
        root.title("Covid-19 Expert System")
        self.levels = len(levels_with_questions)
        self.current_level = 0
        self.vars = []
        self.ask_level()

    def ask_level(self):
        data = levels_with_questions[self.current_level]
        # clear previous widgets
        for w in self.root.winfo_children():
            w.destroy()

        # header
        tk.Label(self.root,
                 text=f"Level {data['level']}: {data['level_title']}",
                 font=("Helvetica", 20)
        ).pack(pady=10)

        # questions
        self.vars.clear()
        for q in data["questions"]:
            frame = tk.Frame(self.root)
            frame.pack(anchor="w", padx=10, pady=5)
            tk.Label(frame, text=q["question"]).pack(anchor="w")

            # default to first option key to avoid KeyError
            first_opt = next(iter(q["options"]))
            var = tk.StringVar(value=first_opt)
            self.vars.append((var, q["options"]))

            for opt_label in q["options"]:
                tk.Radiobutton(frame, text=opt_label, variable=var, value=opt_label).pack(anchor="w")

        # next/finish button
        btn_text = "Next" if self.current_level < self.levels - 1 else "Finish"
        tk.Button(self.root, text=btn_text, command=self.next_level).pack(pady=20)

    def next_level(self):
        # score this level
        score = sum(options[var.get()] for var, options in self.vars)
        setattr(self, f"level{self.current_level+1}_score", score)

        self.current_level += 1
        if self.current_level < self.levels:
            self.ask_level()
        else:
            self.evaluate()

    def evaluate(self):
        total = sum(getattr(self, f"level{i+1}_score") for i in range(self.levels))
        engine = CovidExpertSystem()
        engine.reset()
        engine.declare(Fact(total_score=total))
        engine.run()

        risk = engine.risk_result or "Unknown"
        messagebox.showinfo("Diagnosis Result",
                            f"Total Score: {total}\nCovid-19 Risk: {risk}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CovidDiagnosisApp(root)
    root.mainloop()