from rolepermissions.roles import AbstractUserRole


class Proprietario(AbstractUserRole):
    available_permissions = {
        'Cadastrar_casas': True,
        'excluir_casas':True,
        'editar_casas':True,
    }

class Locatario(AbstractUserRole):
    available_permissions = {
        'Fazer_reservas': True,
        'cancelar_reservas':True,

    }
