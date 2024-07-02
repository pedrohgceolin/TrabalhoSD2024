import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tabulate import tabulate
import random
import time

class Processo:
    def __init__(self, id, ativo=True):
        self.id = id
        self.ativo = ativo

    def __str__(self):
        return f"Processo {self.id}"

class Anel:
    def __init__(self):
        self.processos = []
        self.coordenador = None
        self.comunicacao = []
        self.proximo_id = 1

    def adicionar_processo(self):
        processo = Processo(self.proximo_id)
        self.proximo_id += 1
        self.processos.append(processo)
        return processo

    def iniciar_eleicao(self):
        ativos = [p for p in self.processos if p.ativo]
        if not ativos:
            return None

        processo_inicial = random.choice(ativos)
        ids_comunicacao = [processo_inicial.id]
        processo_atual = processo_inicial

        while True:
            proximo_processo = self.get_proximo_processo(processo_atual)
            if proximo_processo and proximo_processo != processo_inicial:
                ids_comunicacao.append(proximo_processo.id)
                self.comunicacao.append((processo_atual.id, ids_comunicacao[:], proximo_processo.id))
                processo_atual = proximo_processo
            else:
                break

        coordenador = max(ativos, key=lambda p: p.id)
        self.coordenador = coordenador
        return coordenador

    def get_proximo_processo(self, processo_atual):
        ativos = [p for p in self.processos if p.ativo and p.id != processo_atual.id]
        if ativos:
            proximo_index = (self.processos.index(processo_atual) + 1) % len(self.processos)
            while not self.processos[proximo_index].ativo:
                proximo_index = (proximo_index + 1) % len(self.processos)
            return self.processos[proximo_index]
        return None

    def falha_lider(self):
        if self.coordenador and self.coordenador.ativo:
            lider_falho = self.coordenador
            lider_falho.ativo = False
            return lider_falho
        return None

    def identificar_falha_e_iniciar_eleicao(self):
        ativos = [p for p in self.processos if p.ativo]
        if ativos:
            processo_que_identificou = random.choice(ativos)
            novo_coordenador = self.iniciar_eleicao()
            return processo_que_identificou, novo_coordenador
        return None, None

    def get_coordenador_atual(self):
        return self.coordenador

    def get_comunicacao(self):
        return self.comunicacao

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Bully Algorithm - Simulação de Eleição de Coordenador")
        self.root.geometry("900x600")  # Ajustando o tamanho da janela principal
        self.anel = Anel()
        self.momento_atual = 0
        self.novo_coordenador = None
        self.historico_eventos = []
        self.init_ui()

    def init_ui(self):
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label_instrucao = ttk.Label(self.frame, text="Clique no botão 'Avançar' para simular cada momento.")
        self.label_instrucao.pack(pady=10)

        self.button_avancar = ttk.Button(self.frame, text="Avançar", command=self.avancar)
        self.button_avancar.pack(pady=10)

        self.table_output = ScrolledText(self.frame, height=20, width=100, wrap=tk.WORD)
        self.table_output.pack(pady=10, expand=True, fill=tk.BOTH)  # Ajustando o tamanho da tabela

        self.label_comunicacao = ttk.Label(self.frame, text="Comunicação:")
        self.label_comunicacao.pack(pady=5)

        self.comunicacao_output = ScrolledText(self.frame, height=10, width=100, wrap=tk.WORD)
        self.comunicacao_output.pack(pady=10, expand=True, fill=tk.BOTH)

        self.atualizar_tabela("Inicialização: Adicione 6 processos para começar.")

    def avancar(self):
        self.momento_atual += 1

        if self.momento_atual == 1:
            # Momento 1: Adicionar 6 processos
            for _ in range(6):
                self.anel.adicionar_processo()
            self.atualizar_tabela("Momento 1: Adicionados 6 processos ao anel.")

        elif self.momento_atual == 2:
            # Momento 2: Iniciar eleição para definir o coordenador
            coordenador = self.anel.iniciar_eleicao()
            if coordenador:
                comunicacao = self.anel.get_comunicacao()
                self.atualizar_tabela(f"Momento 2: Iniciada eleição. Coordenador eleito: {coordenador}", comunicacao)
                self.atualizar_comunicacao(comunicacao)
            else:
                self.atualizar_tabela("Momento 2: Nenhum processo ativo para iniciar a eleição.")

        elif self.momento_atual == 3:
            # Momento 3: Simular falha do líder
            lider_falho = self.anel.falha_lider()
            if lider_falho:
                self.atualizar_tabela(f"Momento 3: Líder {lider_falho} falhou.")
            else:
                self.atualizar_tabela("Momento 3: Não há líder para falhar.")

        elif self.momento_atual == 4:
            # Momento 4: Identificar falha do líder e iniciar nova eleição
            processo_que_identificou, novo_coordenador = self.anel.identificar_falha_e_iniciar_eleicao()
            if processo_que_identificou and novo_coordenador:
                comunicacao = self.anel.get_comunicacao()
                self.atualizar_tabela(f"Momento 4: Processo {processo_que_identificou} identificou a falha. Novo coordenador: {novo_coordenador}", comunicacao)
                self.atualizar_comunicacao(comunicacao)
                self.novo_coordenador = novo_coordenador
            else:
                self.atualizar_tabela("Momento 4: Não foi possível iniciar nova eleição.")

        elif self.momento_atual == 5:
            # Momento 5: Mostrar o resultado da nova eleição
            novo_coordenador = self.anel.get_coordenador_atual()
            if novo_coordenador:
                self.atualizar_tabela(f"Momento 5: Novo coordenador após a eleição: {novo_coordenador}")
                self.novo_coordenador = novo_coordenador
            else:
                self.atualizar_tabela("Momento 5: Nenhum coordenador eleito após a eleição.")

    def atualizar_tabela(self, evento, comunicacao=None):
        self.historico_eventos.append(evento)
        
        headers = ["Momento", "Evento"]
        data = [
            ["1", "Inicialização: Adicione 6 processos para começar."],
            ["2", "Aguardando ação..."],
            ["3", "Aguardando ação..."],
            ["4", "Aguardando ação..."],
            ["5", "Aguardando ação..."]
        ]

        for i in range(min(len(self.historico_eventos), 5)):
            data[i][1] = self.historico_eventos[i]

        table = tabulate(data, headers, tablefmt="grid")
        self.table_output.delete(1.0, tk.END)
        self.table_output.insert(tk.END, table)

    def atualizar_comunicacao(self, comunicacao):
        self.comunicacao_output.configure(state=tk.NORMAL)
        self.comunicacao_output.delete(1.0, tk.END)
        for com in comunicacao:
            self.comunicacao_output.insert(tk.END, f"{com}\n")
        self.comunicacao_output.configure(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
