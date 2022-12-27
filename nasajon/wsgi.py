# Importando arquivos de configuração
from nasajon.settings import DEBUG, SERVER_PORT, application
import nasajon.db_pool_config

# TODO Importar todos os controllers (se não, as rotas não existirão)
import nasajon.controller.planta_controller
import nasajon.controller.centro_de_trabalho_controller

if __name__ == '__main__':
    application.run(port=SERVER_PORT, host="0.0.0.0", debug=DEBUG)
    # application.run(port=SERVER_PORT)

