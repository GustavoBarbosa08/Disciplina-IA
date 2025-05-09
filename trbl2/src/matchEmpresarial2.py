#Sistema Especialista para Recrutamento e Seleção de Vagas
# Gustavo Barbosa Neves 
# Thalles Augusto Monteiro Martins 

from experta import Fact, KnowledgeEngine, Rule
import tkinter as tk
from tkinter import ttk, messagebox

# --------------------------- FATOS ---------------------------
class Candidato(Fact):
    """Descreve o perfil do candidato."""

# ------------------- BASE DE CONHECIMENTO --------------------
BACKEND_PYTHON = {
    'linguagens':        (lambda l: 'python' in [x.lower() for x in l], 2),
    'frameworks':        (lambda f: 'django'  in [x.lower() for x in f], 2),
    'experiencia':       (lambda x: x >= 3, 3),
    'tipo_contratacao':  (lambda x: x == 'pj', 1),
    'localizacao':       (lambda x: x == 'remoto', 1),
    'ingles':            (lambda i: i in {'intermediário', 'avançado'}, 1),
    'pretensao_salarial':(lambda s: s <= 8000, 2),
    'formacao':          (lambda f: f in {'graduação', 'mestrado'}, 1)
}

FRONTEND_REACT = {
    'linguagens':        (lambda l: 'javascript' in [x.lower() for x in l], 2),
    'frameworks':        (lambda f: 'react' in [x.lower() for x in f], 2),
    'experiencia':       (lambda x: x >= 2, 2),
    'tipo_contratacao':  (lambda x: x == 'clt', 1),
    'localizacao':       (lambda x: x == 'hibrido', 1),
    'pretensao_salarial':(lambda s: s <= 6000, 2),
    'formacao':          (lambda f: f in {'técnico', 'graduação'}, 1)
}

FULLSTACK = {
    'linguagens':        (lambda l: {'python','javascript'}.issubset({x.lower() for x in l}), 3),
    'frameworks':        (lambda f: {'django','react'}.issubset({x.lower() for x in f}), 3),
    'experiencia':       (lambda x: x >= 4, 3),
    'tipo_contratacao':  (lambda x: x == 'pj', 1),
    'localizacao':       (lambda x: x == 'remoto', 1),
    'pretensao_salarial':(lambda s: s <= 10000, 2),
    'formacao':          (lambda f: f in {'graduação', 'mestrado'}, 1)
}

BACKEND_JAVA = {
    'linguagens':        (lambda l: 'java' in [x.lower() for x in l], 3),
    'experiencia':       (lambda x: x >= 5, 3),
    'tipo_contratacao':  (lambda x: x == 'clt', 1),
    'localizacao':       (lambda x: x == 'presencial', 1),
    'pretensao_salarial':(lambda s: s <= 9000, 2),
    'formacao':          (lambda f: f in {'graduação', 'mestrado'}, 1)
}

FRONTEND_NEXT = {
    'linguagens':        (lambda l: 'typescript' in [x.lower() for x in l], 2),
    'frameworks':        (lambda f: 'next.js' in [x.lower() for x in f], 2),
    'experiencia':       (lambda x: x >= 1, 1),
    'tipo_contratacao':  (lambda x: x == 'pj', 1),
    'localizacao':       (lambda x: x == 'remoto', 1),
    'pretensao_salarial':(lambda s: s <= 7000, 5),
    'formacao':          (lambda f: f in {'técnico', 'graduação'}, 1)
}

DEVOPS_AWS = {
    'linguagens':        (lambda l: bool({'python','bash'} & {x.lower() for x in l}), 1),
    'ferramentas':       (lambda t: {'docker','kubernetes'}.issubset({x.lower() for x in t}), 3),
    'cloud':             (lambda c: 'aws' in [x.lower() for x in c], 3),
    'certificacoes':     (lambda c: 'aws certified' in [x.lower() for x in c], 2),
    'experiencia':       (lambda x: x >= 3, 3),
    'tipo_contratacao':  (lambda x: x == 'pj', 1),
    'localizacao':       (lambda x: x == 'remoto', 1),
    'ingles':            (lambda i: i == 'avançado', 1),
    'pretensao_salarial':(lambda s: s <= 11000, 2),
    'formacao':          (lambda f: f in {'graduação', 'mestrado'}, 1)
}

DATA_SCIENTIST = {
    'linguagens':        (lambda l: 'python' in [x.lower() for x in l], 2),
    'ferramentas':       (lambda t: {'pandas','scikit-learn'}.issubset({x.lower() for x in t}), 3),
    'experiencia':       (lambda x: x >= 2, 2),
    'tipo_contratacao':  (lambda x: x == 'clt', 1),
    'localizacao':       (lambda x: x == 'presencial', 1),
    'ingles':            (lambda i: i in {'intermediário','avançado'}, 1),
    'pretensao_salarial':(lambda s: s <= 9000, 2),
    'formacao':          (lambda f: f in {'mestrado','doutorado'}, 2)
}

QA_AUTOMATION = {
    'linguagens':        (lambda l: bool({'python','javascript'} & {x.lower() for x in l}), 1),
    'ferramentas':       (lambda t: {'selenium','pytest'}.issubset({x.lower() for x in t}), 3),
    'experiencia':       (lambda x: x >= 2, 2),
    'tipo_contratacao':  (lambda x: x == 'clt', 1),
    'localizacao':       (lambda x: x == 'hibrido', 1),
    'pretensao_salarial':(lambda s: s <= 6000, 2),
    'formacao':          (lambda f: f in {'técnico','graduação'}, 1)
}

MOBILE_FLUTTER = {
    'linguagens':        (lambda l: 'dart' in [x.lower() for x in l], 2),
    'frameworks':        (lambda f: 'flutter' in [x.lower() for x in f], 3),
    'experiencia':       (lambda x: x >= 2, 2),
    'tipo_contratacao':  (lambda x: x == 'pj', 1),
    'localizacao':       (lambda x: x == 'remoto', 1),
    'pretensao_salarial':(lambda s: s <= 8000, 2),
    'formacao':          (lambda f: f in {'técnico','graduação'}, 1)
}

VAGAS = [
    ("DevOps AWS (Remoto, PJ)",                DEVOPS_AWS,    8),
    ("Data Scientist (Presencial, CLT)",       DATA_SCIENTIST,7),
    ("Backend Python (Django, Remoto, PJ)",    BACKEND_PYTHON,6),
    ("Full-Stack Django + React (Remoto, PJ)", FULLSTACK,     5),
    ("Frontend React (Híbrido, CLT)",          FRONTEND_REACT,4),
    ("Backend Java Enterprise (Presencial)",   BACKEND_JAVA,  3),
    ("QA Automation (Híbrido, CLT)",           QA_AUTOMATION, 2),
    ("Frontend Next.js (Remoto, PJ)",          FRONTEND_NEXT, 1),
    ("Mobile Flutter (Remoto, PJ)",            MOBILE_FLUTTER,0),
]

# ----------------- MOTOR ESPECIALISTA ------------------------
class MotorVagas(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resultados = []

    @staticmethod
    def _pontuar(cand, criterios):
        pontos = peso_total = 0
        for campo, (cond, peso) in criterios.items():
            valor = cand.get(campo)
            if valor:                         # só considerar o peso se o campo veio preenchido
                peso_total += peso
                if cond(valor):
                    pontos += peso
        return round((pontos / peso_total) * 100, 2) if peso_total else 0

    # ---------- Regras manuais ----------
    @Rule(Candidato(), salience=8)
    def vaga_devops_aws(self):
        p = self._pontuar(self.facts[1], DEVOPS_AWS)
        if p: self.resultados.append((VAGAS[0][0], p))

    @Rule(Candidato(), salience=7)
    def vaga_data_scientist(self):
        p = self._pontuar(self.facts[1], DATA_SCIENTIST)
        if p: self.resultados.append((VAGAS[1][0], p))

    @Rule(Candidato(), salience=6)
    def vaga_backend_python(self):
        p = self._pontuar(self.facts[1], BACKEND_PYTHON)
        if p: self.resultados.append((VAGAS[2][0], p))

    @Rule(Candidato(), salience=5)
    def vaga_fullstack(self):
        p = self._pontuar(self.facts[1], FULLSTACK)
        if p: self.resultados.append((VAGAS[3][0], p))

    @Rule(Candidato(), salience=4)
    def vaga_frontend_react(self):
        p = self._pontuar(self.facts[1], FRONTEND_REACT)
        if p: self.resultados.append((VAGAS[4][0], p))

    @Rule(Candidato(), salience=3)
    def vaga_backend_java(self):
        p = self._pontuar(self.facts[1], BACKEND_JAVA)
        if p: self.resultados.append((VAGAS[5][0], p))

    @Rule(Candidato(), salience=2)
    def vaga_qa_automation(self):
        p = self._pontuar(self.facts[1], QA_AUTOMATION)
        if p: self.resultados.append((VAGAS[6][0], p))

    @Rule(Candidato(), salience=1)
    def vaga_frontend_next(self):
        p = self._pontuar(self.facts[1], FRONTEND_NEXT)
        if p: self.resultados.append((VAGAS[7][0], p))

    @Rule(Candidato(), salience=0)
    def vaga_mobile_flutter(self):
        p = self._pontuar(self.facts[1], MOBILE_FLUTTER)
        if p: self.resultados.append((VAGAS[8][0], p))

    def resultados_ordenados(self):
        return sorted(self.resultados, key=lambda x: -x[1])

# ----------------------- GUI ---------------------------------
LINGUAGENS = ['Python', 'JavaScript', 'TypeScript', 'Java', 'C#',
              'PHP', 'Ruby', 'Go', 'Bash', 'Dart']
FRAMEWORKS = ['Django', 'React', 'Next.js', 'Angular', 'Vue.js',
              'Flask', 'Spring', 'Laravel', 'Ruby on Rails', 'Flutter']
FERRAMENTAS = ['Docker', 'Kubernetes', 'Selenium', 'PyTest',
               'Pandas', 'Scikit-learn', 'TensorFlow']
CLOUD_PROVIDERS = ['AWS', 'Azure', 'GCP']
CERTIFICACOES = ['AWS Certified', 'Azure Fundamentals', 'Scrum Master']

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Vagas – Avaliação de Candidato")
        self.geometry("950x780")
        self.resizable(False, False)

        frm = ttk.LabelFrame(self, text="Dados do Candidato")
        frm.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------- Linguagens ----------
        ttk.Label(frm, text="Linguagens:").grid(row=0, column=0, sticky="nw")
        self.lang_vars = {}
        for i, lang in enumerate(LINGUAGENS):
            var = tk.BooleanVar()
            ttk.Checkbutton(frm, text=lang, variable=var)\
               .grid(row=0 + i//6, column=1 + i%6, sticky="w")
            self.lang_vars[lang] = var

        # ---------- Frameworks ----------
        off_row = (len(LINGUAGENS)-1)//6 + 2
        ttk.Label(frm, text="Frameworks:").grid(row=off_row, column=0, sticky="nw")
        self.fw_vars = {}
        for i, fw in enumerate(FRAMEWORKS):
            var = tk.BooleanVar()
            ttk.Checkbutton(frm, text=fw, variable=var)\
               .grid(row=off_row + i//6, column=1 + i%6, sticky="w")
            self.fw_vars[fw] = var

        # ---------- Ferramentas ----------
        row_tools = off_row + (len(FRAMEWORKS)-1)//6 + 2
        ttk.Label(frm, text="Ferramentas:").grid(row=row_tools, column=0, sticky="nw")
        self.tool_vars = {}
        for i, tool in enumerate(FERRAMENTAS):
            var = tk.BooleanVar()
            ttk.Checkbutton(frm, text=tool, variable=var)\
               .grid(row=row_tools + i//6, column=1 + i%6, sticky="w")
            self.tool_vars[tool] = var

        # ---------- Cloud ----------
        row_cloud = row_tools + (len(FERRAMENTAS)-1)//6 + 2
        ttk.Label(frm, text="Cloud:").grid(row=row_cloud, column=0, sticky="nw")
        self.cloud_vars = {}
        for i, cloud in enumerate(CLOUD_PROVIDERS):
            var = tk.BooleanVar()
            ttk.Checkbutton(frm, text=cloud, variable=var)\
               .grid(row=row_cloud, column=1 + i, sticky="w")
            self.cloud_vars[cloud] = var

        # ---------- Certificações ----------
        row_cert = row_cloud + 2
        ttk.Label(frm, text="Certificações:").grid(row=row_cert, column=0, sticky="nw")
        self.cert_vars = {}
        for i, cert in enumerate(CERTIFICACOES):
            var = tk.BooleanVar()
            ttk.Checkbutton(frm, text=cert, variable=var)\
               .grid(row=row_cert + i//3, column=1 + i%3, sticky="w")
            self.cert_vars[cert] = var

        # ---------- Campos numéricos / escolha única ----------
        row_base = row_cert + (len(CERTIFICACOES)-1)//3 + 2

        ttk.Label(frm, text="Experiência (anos):")\
            .grid(row=row_base, column=0, sticky="e")
        self.ent_exp = ttk.Spinbox(frm, from_=0, to=40, width=6)
        self.ent_exp.grid(row=row_base, column=1, sticky="w")

        ttk.Label(frm, text="Tipo de contratação:")\
            .grid(row=row_base+1, column=0, sticky="e")
        self.tipo_var = tk.StringVar()
        for i, t in enumerate(("pj","clt")):
            ttk.Radiobutton(frm, text=t.upper(), variable=self.tipo_var, value=t)\
               .grid(row=row_base+1, column=1+i, sticky="w")

        ttk.Label(frm, text="Localização:")\
            .grid(row=row_base+2, column=0, sticky="e")
        self.loc_var = tk.StringVar()
        for i, loc in enumerate(("remoto","hibrido","presencial")):
            ttk.Radiobutton(frm, text=loc.capitalize(), variable=self.loc_var, value=loc)\
               .grid(row=row_base+2, column=1+i, sticky="w")

        ttk.Label(frm, text="Inglês:")\
            .grid(row=row_base+3, column=0, sticky="e")
        self.eng_var = tk.StringVar()
        for i, lvl in enumerate(("básico","intermediário","avançado")):
            ttk.Radiobutton(frm, text=lvl.capitalize(), variable=self.eng_var, value=lvl)\
               .grid(row=row_base+3, column=1+i, sticky="w")

        ttk.Label(frm, text="Pretensão Salarial (R$):")\
            .grid(row=row_base+4, column=0, sticky="e")
        self.ent_sal = ttk.Spinbox(frm, from_=1000, to=30000, increment=500, width=8)
        self.ent_sal.grid(row=row_base+4, column=1, sticky="w")

        ttk.Label(frm, text="Formação:")\
            .grid(row=row_base+5, column=0, sticky="e")
        self.form_var = tk.StringVar()
        for i, form in enumerate(("técnico","graduação","mestrado","doutorado")):
            ttk.Radiobutton(frm, text=form.capitalize(), variable=self.form_var, value=form)\
               .grid(row=row_base+5, column=1+i, sticky="w")

        # ---------- Botão e resultados ----------
        ttk.Button(self, text="Avaliar Vagas", command=self.avaliar)\
            .pack(pady=10)
        self.txt_res = tk.Text(self, height=12, width=110, state="disabled")
        self.txt_res.pack(padx=10, pady=10, fill="both", expand=True)

    # ---------------- Avaliação -----------------
    def avaliar(self):
        try:
            exp = int(self.ent_exp.get())
            sal = int(self.ent_sal.get())
        except ValueError:
            messagebox.showwarning("Atenção", "Experiência e salário precisam ser numéricos.")
            return

        obrigatorios = [self.tipo_var.get(), self.loc_var.get(),
                        self.eng_var.get(),  self.form_var.get()]
        if not all(obrigatorios):
            messagebox.showwarning("Atenção", "Preencha todas as opções obrigatórias.")
            return

        linguagens   = [k for k,v in self.lang_vars.items()  if v.get()]
        if not linguagens:
            messagebox.showwarning("Atenção", "Selecione pelo menos uma linguagem.")
            return

        frameworks   = [k for k,v in self.fw_vars.items()    if v.get()]
        ferramentas  = [k for k,v in self.tool_vars.items()  if v.get()]
        cloud        = [k for k,v in self.cloud_vars.items() if v.get()]
        certificacoes= [k for k,v in self.cert_vars.items()  if v.get()]

        cand = {
            'linguagens': linguagens,
            'frameworks': frameworks,
            'ferramentas': ferramentas,
            'cloud': cloud,
            'certificacoes': certificacoes,
            'experiencia': exp,
            'tipo_contratacao': self.tipo_var.get(),
            'localizacao': self.loc_var.get(),
            'ingles': self.eng_var.get(),
            'pretensao_salarial': sal,
            'formacao': self.form_var.get()
        }

        engine = MotorVagas()
        engine.reset()
        engine.declare(Candidato(**cand))
        engine.run()

        self.txt_res.config(state="normal")
        self.txt_res.delete("1.0", tk.END)
        if not engine.resultados:
            self.txt_res.insert(tk.END, "Nenhuma vaga compatível.\n")
        else:
            self.txt_res.insert(tk.END, "Compatibilidade encontrada:\n\n")
            for vaga, pct in engine.resultados_ordenados():
                self.txt_res.insert(tk.END, f"- {vaga}: {pct}%\n")
        self.txt_res.config(state="disabled")

# --------------------------- MAIN -----------------------------
if __name__ == "__main__":
    App().mainloop()
