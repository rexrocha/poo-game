import json
import os
import traceback

class SalvarCarregar:
    def __init__(self):
        self.__arquivo = "save.json"

    @property
    def arquivo(self):
        return self.__arquivo

    def salvar(self, dados: dict) -> None:
        try:
            os.makedirs(os.path.dirname(self.__arquivo) or '.', exist_ok=True)
            with open(self.__arquivo, "w") as f:
                json.dump(dados, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            traceback.print_exc()

    def carregar(self) -> dict:
        try:
            default_data = {
                "score": 0,
                "vida": 3,
                "pos_x": 400,
                "pos_y": 500,
                "tipo_jogador": 1
            }

            if not os.path.exists(self.__arquivo):
                return default_data
            
            with open(self.__arquivo, "r") as f:
                dados = json.load(f)
                required_keys = ["score", "vida", "pos_x", "pos_y", "tipo_jogador"]
                if not all(key in dados for key in required_keys):
                    raise ValueError("Dados incompletos ou corrompidos no arquivo de save")
                return dados
        except Exception as e:
            print(f"Erro ao carregar save: {e}")
            traceback.print_exc()
            return {
                "score": 0,
                "vida": 3,
                "pos_x": 400,
                "pos_y": 500,
                "tipo_jogador": 1
            }