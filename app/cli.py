from datetime import datetime, timedelta
from app.models import FoodItem
from app.auth.email import send_expiry_alert_email

def register_commands(app):
    @app.cli.command('send-expiry-alerts')
    def send_expiry_alerts():
        """
        Encontra alimentos próximos ao vencimento e envia e-mails de alerta.
        Roda uma vez ao dia.
        """
        print("Iniciando verificação de alimentos próximos ao vencimento")

        with app.app_context():
            seven_days_from_now = datetime.utcnow().date() + timedelta(days=7)

            # Busca todos os itens que vencem entre hoje e os próximos 7 dias
            expiring_items = FoodItem.query.filter(
                FoodItem.expiry_date <= seven_days_from_now,
                FoodItem.expiry_date>= datetime.utcnow().date()
            ).order_by(FoodItem.user_id, FoodItem.expiry_date).all()

            if not expiring_items:
                print("Nenhum item próximo ao vencimento encontrado. Finalizando")
                return
            
            print(f"Encontrados {len(expiring_items)} itens próximos ao vencimento...")

            # Dicionário para agrupar itens por usuários
            users_to_notify = {}
        
            for item in expiring_items:
                # Se o usuário ainda não está no nosso dicionário, adiconamos ele
                if item.owner not in users_to_notify:
                    users_to_notify[item.owner] = []
                # Adiciona o item à lista daquele usuário
                users_to_notify[item.owner].append(item)
            
            for user, items in users_to_notify.items():
                send_expiry_alert_email(user, items)
                print(f"E-mail de alerta enviado para {user.username} com {len(items)} item(ns).")
            
        print("Verificação concluída.")

        