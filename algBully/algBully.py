import random
import tkinter as tk
from tkinter import ttk
from threading import Thread, Event, Lock
from tabulate import tabulate
from termcolor import colored
import time

class Processo:
    def __init__(self, id, ativar=True):
        self.id = id
        self.ativar = ativar

    def __str__(self):
        return f"Processo {self.id}"

    def executar(self):
        print(f"{self} está executando sua tarefa.")
        time.sleep(1)

class Anel:
    def __init__(self):
        self.processos = []
        self.coordenador = None
        self.lock = Lock()
        self.proximo_processo_id = 1  # Controle do próximo ID do processo
        self.comunicacao = []  # Lista para rastrear a comunicação entre processos
        self.processo_que_identificou_falha = None  # Para rastrear qual processo identificou a falha

    def adicionar_processo(self, processo):
        with self.lock:
            self.processos.append(processo)
            print(f"{processo} foi adicionado ao anel")

    def iniciar_eleicao(self, processo_inicial=None):
        with self.lock:
            ativos = [p for p in self.processos if p.ativar]
            if not ativos:
                print("Sem processos ativos para iniciar a eleição")
                return None

            if processo_inicial is None:
                processo_inicial = random.choice(ativos)
            print(f"O processo {processo_inicial} iniciará a eleição.")

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
            print(f"{coordenador} se tornou o coordenador")
            self.coordenador = coordenador  # Definir o coordenador atual
            return coordenador

    def get_proximo_processo(self, processo_atual):
        ativos = [p for p in self.processos if p.ativar and p.id != processo_atual.id]
        if ativos:
            proximo_index = (self.processos.index(processo_atual) + 1) % len(self.processos)
            while not self.processos[proximo_index].ativar:
                proximo_index = (proximo_index + 1) % len(self.processos)
            return self.processos[proximo_index]
        return None

    def falhar_lider(self):
        with self.lock:
            if self.coordenador and self.coordenador.ativar:
                coordenador_falho = self.coordenador
                coordenador_falho.ativar = False
                print(f"Líder {coordenador_falho} falhou.")
                self.processo_que_identificou_falha = random.choice([p for p in self.processos if p.ativar and p != coordenador_falho])
                return coordenador_falho
            return None

    def iniciar_nova_eleicao(self):
        with self.lock:
            if self.processo_que_identificou_falha:
                processo_que_identificou = self.processo_que_identificou_falha
                self.processo_que_identificou_falha = None  # Limpar o processo que identificou a falha
                print(f"Processo {processo_que_identificou} identificou a falha e iniciou nova eleição.")
                novo_coordenador = self.iniciar_eleicao()
                if novo_coordenador:
                    self.coordenador = novo_coordenador
                    return processo_que_identificou, novo_coordenador
            return None

    def selecionar_processo_aleatorio(self):
        with self.lock:
            ativos = [p for p in self.processos if p.ativar]
            if ativos:
                return random.choice(ativos)
            return None

    def atualizar_tabela(self):
        # Cria e atualiza a tabela de comunicação
        headers = [colored("Processo Atual", "cyan"), colored("Comunicação", "cyan"), colored("Ref. de Saída", "cyan")]
        table_data = []
        for processo_atual, mensagem, ref_saida in self.comunicacao:
            mensagem_str = ",".join(map(str, mensagem))
            table_data.append([colored(processo_atual, "green"), colored(mensagem_str, "magenta"), colored(ref_saida, "green")])
        tabela = tabulate(table_data, headers, tablefmt="fancy_grid")
        return tabela

class App:
    def __init__(self, root, anel):
        self.root = root
        self.root.title("Bully Algorithm - Eleição de Coordenador")
        self.anel = anel
        self.momento_atual = 0  # Controla o momento atual
        self.init_ui()

    def init_ui(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.button_avancar = ttk.Button(self.frame, text="Avançar", command=self.avancar)
        self.button_avancar.pack(pady=5)

        self.text_output = tk.Text(self.frame, height=20, width=60)
        self.text_output.pack(pady=10)

    def avancar(self):
        self.momento_atual += 1

        if self.momento_atual == 1:
            # Momento 1: Adicionar 6 processos
            for i in range(1, 7):
                novo_processo = Processo(id=i)
                self.anel.adicionar_processo(novo_processo)
                self.text_output.insert(tk.END, f"{novo_processo} foi adicionado ao anel\n")
            self.text_output.insert(tk.END, "\n--- Momento 1: Adicionados 6 processos ---\n\n")

        elif self.momento_atual == 2:
            # Momento 2: Iniciar eleição para definir o coordenador
            coordenador = self.anel.iniciar_eleicao()
            if coordenador:
                self.text_output.insert(tk.END, f"O coordenador eleito é o {coordenador}\n")
            else:
                self.text_output.insert(tk.END, "Nenhum processo ativo para iniciar a eleição\n")
            self.text_output.insert(tk.END, "\n--- Momento 2: Eleição de coordenador ---\n\n")

        elif self.momento_atual == 3:
            # Momento 3: Simular falha do líder e identificar processo falho
            coordenador_falho = self.anel.falhar_lider()
            if coordenador_falho:
                self.text_output.insert(tk.END, f"Líder {coordenador_falho} falhou\n")
                if self.anel.processo_que_identificou_falha:
                    processo_que_identificou, novo_coordenador = self.anel.iniciar_nova_eleicao()
                    if processo_que_identificou and novo_coordenador:
                        self.text_output.insert(tk.END, f"Processo {processo_que_identificou} identificou a falha e iniciou nova eleição\n")
                        self.text_output.insert(tk.END, f"Novo coordenador eleito: {novo_coordenador}\n")
                    else:
                        self.text_output.insert(tk.END, "Não foi possível iniciar nova eleição\n")
                else:
                    self.text_output.insert(tk.END, "Nenhum processo identificou a falha\n")
            else:
                self.text_output.insert(tk.END, "Não há líder para falhar\n")
            self.text_output.insert(tk.END, "\n--- Momento 3: Líder falhou ---\n\n")

        elif self.momento_atual == 4:
            # Momento 4: Mostrar o novo coordenador eleito após a eleição
            if self.anel.coordenador:
                self.text_output.insert(tk.END, f"Novo coordenador eleito: {self.anel.coordenador}\n")
            else:
                self.text_output.insert(tk.END, "Nenhum novo coordenador foi eleito\n")
            self.text_output.insert(tk.END, "\n--- Momento 4: Novo coordenador eleito ---\n\n")

        else:
            self.text_output.insert(tk.END, "Todos os momentos concluídos.\n")

        self.text_output.see(tk.END)  # Rolagem automática para a última linha

        # Atualizar a interface gráfica após cada momento
        self.root.after(100, self.update_gui)

    def update_gui(self):
        # Atualiza a interface com a tabela de comunicação
        tabela = self.anel.atualizar_tabela()
        self.text_output.insert(tk.END, tabela + "\n")
        self.text_output.see(tk.END)  # Rolagem automática para a última linha

if __name__ == "__main__":
    anel = Anel()

    root = tk.Tk()
    app = App(root, anel)
    root.mainloop()
