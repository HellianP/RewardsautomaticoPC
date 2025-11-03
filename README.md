# Auto-Clicker & Typer Script

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Um script simples em Python que automatiza a tarefa de clicar em uma posição específica da tela, digitar uma sequência numérica e pressionar "Enter". Ideal para automatizar tarefas repetitivas e monótonas.

## 📖 Descrição

Este script utiliza as bibliotecas `pyautogui` para controlar o mouse e o teclado e `pynput` para ouvir eventos do teclado. Ao ser executado, ele oferece 5 segundos para que o usuário posicione o mouse no local desejado. Após capturar as coordenadas, o script inicia um loop que clica, digita um número sequencial (de 0 a 32) e pressiona Enter, com pausas para garantir a compatibilidade com diferentes sistemas.

A execução pode ser interrompida a qualquer momento de forma segura.

## ✨ Funcionalidades Principais

- **Captura Dinâmica de Posição:** Define o local dos cliques com base na posição do mouse no início da execução.
- **Automação de Tarefas:** Executa cliques, digitação de uma sequência numérica e pressionamento da tecla `Enter`.
- **Contador de Progresso:** Exibe o número atual da sequência e uma estimativa do tempo restante para a conclusão.
- **Mecanismos de Parada de Emergência:**
    1.  **Parada Controlada:** Pressione a tecla **`Espaço`** para interromper o script de forma limpa.
    2.  **FAILSAFE (PyAutoGUI):** Mova o cursor do mouse rapidamente para o **canto superior esquerdo** da tela para forçar o encerramento.

## ⚙️ Pré-requisitos

Antes de executar o script, certifique-se de que você tem o Python instalado em seu sistema. Você precisará instalar as seguintes bibliotecas:

- `pyautogui`: Para automação da GUI.
- `pynput`: Para capturar eventos do teclado.

### Instalação

Abra o seu terminal ou prompt de comando e instale as dependências usando `pip`:

```bash
pip install pyautogui pynput

🚀 Como Usar
Clone o repositório ou salve o código em um arquivo local, por exemplo, auto_typer.py.

Execute o script através do terminal:

Bash

python auto_typer.py
Após a execução, a seguinte mensagem aparecerá no terminal:

Posicione o mouse no local desejado em 5 segundos...
Mova o cursor do mouse para a exata posição na tela onde você deseja que os cliques ocorram (por exemplo, dentro de uma caixa de texto).

Aguarde 5 segundos sem mover o mouse. O script capturará as coordenadas e iniciará o processo de automação.

O script começará a clicar, digitar os números de 0 a 32 e pressionar Enter no local definido.

🛑 Como Parar a Execução
Você pode interromper o script a qualquer momento usando um dos dois métodos:

Pressione a tecla Espaço: O programa exibirá uma mensagem de interrupção e será encerrado de forma segura.

Mova o mouse para o canto superior esquerdo da tela: Este é um recurso de segurança da biblioteca pyautogui e irá gerar um erro pyautogui.FailSafeException, encerrando o script imediatamente.

⚠️ Aviso Importante
Este script foi projetado para controlar seu mouse e teclado. Durante sua execução, evite usar o computador para outras tarefas, pois o script pode interferir na sua utilização. Use-o com responsabilidade e sempre monitore sua execução. O desenvolvedor não se responsabiliza por qualquer uso indevido ou consequências inesperadas.