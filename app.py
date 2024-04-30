from flask import Flask, render_template, request
import stripe

app = Flask(__name__)

# Configure sua chave secreta do Stripe
stripe.api_key = 'sk_test_51PBIyAGY2TIKtcLFUcPK0KFwQsx86qcurIcaqVvFm6Skjse1v7pAdUFBG9wuxmOAZEEtU1DHsQplIwXqe5nbv4SE006N9tCclr'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cobrar', methods=['POST'])
def cobrar():
    # Obter o token do cartão do formulário
    token = request.form['stripeToken']

    # Criar uma cobrança usando o token
    try:
        charge = stripe.Charge.create(
            amount=1000,  # Valor em centavos (R$ 10,00)
            currency='brl',
            description='Exemplo de cobrança',
            source=token,
        )
        mensagem = "Cobrança realizada com sucesso!"
    except stripe.error.StripeError as e:
        mensagem = f"Erro ao realizar a cobrança: {e.error.message}"

    return render_template('resultado.html', mensagem=mensagem)


if __name__ == '__main__':
    app.run(debug=True)
