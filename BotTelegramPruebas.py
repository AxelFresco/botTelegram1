from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random
from telegram.ext import ConversationHandler
import logging
import datetime

TOKEN = '7240801167:AAElezmbVvapp1alYWMlMfUoGPflFVTQfaA'
#--------------------------------------------------------------Base de conocimiento con posibles respuestas
knowledge_base = {
    'What color is the sky?': ['blue', 'Blue', 'light blue', 'Light Blue', 'Light blue'],
    'What is the sum of 1 + 1?': ['2', 'two', 'Two', 'dos', 'Dos'],
    'What is the name of this chat?': ['manuel', 'Manuel']
}
#----------------------------------------------------------------Trivia Repuestas
trivia_questions = [
    {
        'question': "¿Cuál es la capital de Francia?",
        'options': ['París', 'Londres', 'Madrid'],
        'answer': 'París'
    },
    {
        'question': "¿Cuál es el planeta más cercano al Sol?",
        'options': ['Venus', 'Marte', 'Mercurio'],
        'answer': 'Mercurio'
    },
    {
        'question': "¿Quién pintó la Mona Lisa?",
        'options': ['Vincent van Gogh', 'Leonardo da Vinci', 'Pablo Picasso'],
        'answer': 'Leonardo da Vinci'
    }
]
#----------------------------------------------------------------Información de productos
products = [
    {
        'name': 'Producto 1',
        'description': 'Descripción del Producto 1',
        'price': '$10.00',
        'image_url': 'https://ibb.co/SJ3xz8t',
        'cantidad':'10',
        'CAD':'05/11/2025'
    },
    {
        'name': 'Producto 2',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/z7B3b0X',
        'cantidad':'10',
        'CAD':'05/11/2030'
    },
    {
        'name': 'Producto 3',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/WtPf8yc',
        'cantidad':'10',
        'CAD':'05/11/2031'
    },
    {
        'name': 'Producto 4',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/SJ3xz8t',
        'cantidad':'10',
        'CAD':'05/11/2026'
    },
    {
        'name': 'Producto 5',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/SJ3xz8t',
        'cantidad':'10',
        'CAD':'05/11/2025'
    },
    {
        'name': 'Producto 6',
        'description': 'Descripción del Producto 1',
        'price': '$20.00',
        'image_url': 'https://ibb.co/SJ3xz8t',
        'cantidad':'10',
        'CAD':'05/11/2025'
    },
]
#----------------------------------------------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("MAIN MENU\nChoose option: ", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text("Choose option: ", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button press."""
    query = update.callback_query
    await query.answer()

    if query.data == '1':
        # Create a submenu for Option 2
        response = "HELLO, WELCOME"
#----------------------------------------------------------------------------------------------------------------------    
    elif query.data == '2':
        # Create a submenu for Option 2
        keyboard = [
            [
                InlineKeyboardButton("Pregunta 1", callback_data='2.1'),
                InlineKeyboardButton("Pregunta 2", callback_data='2.2'),
                InlineKeyboardButton("Pregunta 3", callback_data='2.3'),
                InlineKeyboardButton("Traductor (Anuncio)", callback_data='2.4'),
                InlineKeyboardButton("Trivia", callback_data='2.5'),
                InlineKeyboardButton("Catalogo", callback_data='2.6'),
                InlineKeyboardButton("Interacción con Manuel", callback_data='2.7')
            ],
            [InlineKeyboardButton("Regresar al menu Principal", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="You selected Option 2. Choose a suboption:", reply_markup=reply_markup)
        return
    elif query.data == '2.1':
        question = "What color is the sky?"
        await query.edit_message_text(text=question)
        # Save the correct answer in the context
        context.user_data['correct_answer2.1'] = question
        return
    elif query.data == '2.2':
        question = "What is the sum of 1 + 1?"
        await query.edit_message_text(text=question)
        # Save the correct answer in the context
        context.user_data['correct_answer2.2'] = question
        return
    elif query.data == '2.3':
        question = "What is the name of this chat?"
        await query.edit_message_text(text=question)
        # Save the correct answer in the context
        context.user_data['correct_answer2.3'] = question
        return
    elif query.data == '2.4':
        await send_ads(update, context)
        return  
    elif query.data == '2.5':
        await send_trivia_question(update, context)
        return 
    elif query.data == '2.6':
        await show_products(update, context)
        return 
    elif query.data == '2.7':
        await interaccion_bot(update, context)
        return
    elif query.data == 'main_menu':
        await start(update, context)
        return
    await query.edit_message_text(text=response)

#----------------------------------------------------------------------------------------------------------------------Repuestas preguntas   
async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user's answer to a question."""
    user_answer = update.message.text.strip()
    # Check if there is a current question
    if 'correct_answer2.1' in context.user_data:
        current_question = context.user_data['correct_answer2.1']
      
        # Check if the user's answer matches any of the correct answers
        correct_answers = knowledge_base.get(current_question, [])
        
        if user_answer in correct_answers:
            response = "Correct answer! 🎉"
            await update.message.reply_text(response)
            
            # Remove the stored current question from context
            del context.user_data['correct_answer2.1']
            await start(update, context)
            return
        else:
            response = "Wrong answer. Please try again."
            await update.message.reply_text(response)
            return
    elif 'trivia_question' in context.user_data:
        current_trivia = context.user_data['trivia_question']
    
    # Convert both the user answer and the correct answer to lowercase
        user_answer = update.message.text.strip().lower()
        correct_answer = current_trivia['answer'].lower()

        if user_answer == correct_answer:
            response = "Correct answer! 🎉"
        else:
            response = f"Respuesta incorrecta. La respuesta correcta era {current_trivia['answer']}."
    
        await update.message.reply_text(response)
        
        # Remove the stored trivia question from context
        del context.user_data['trivia_question']
        await start(update, context)
        #--------------------------------------------------------------------------
    if 'correct_answer2.2' in context.user_data:
        current_question = context.user_data['correct_answer2.2']
        
        # Check if the user's answer matches any of the correct answers
        correct_answers = knowledge_base.get(current_question, [])
        
        if user_answer in correct_answers:
            response = "Correct answer! 🎉"
            await update.message.reply_text(response)
            
            # Remove the stored current question from context
            del context.user_data['correct_answer2.2']
            await start(update, context)
            return
        else:
            response = "Wrong answer. Please try again."
            await update.message.reply_text(response)
            return
        #-----------------------------------------------------------------------------
    if 'correct_answer2.3' in context.user_data:
        current_question = context.user_data['correct_answer2.3']
        
        # Check if the user's answer matches any of the correct answers
        correct_answers = knowledge_base.get(current_question, [])
        
        if user_answer in correct_answers:
            response = "Correct answer! 🎉"
            await update.message.reply_text(response)
            
            # Remove the stored current question from context
            del context.user_data['correct_answer2.3']
            await start(update, context)
            return
        else:
            response = "Wrong answer. Please try again."
            await update.message.reply_text(response)
            return
#----------------------------------------------------------------------------------------------------------------------Anuncios internet
async def send_ads(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send advertisements to the user."""
    ads_message = "Esto es un anuncio! 🚀\n\nRevisa nuestras traducciones[Linguee](https://www.linguee.es/espanol-ingles/search?source=auto&query=approximate)."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ads_message)
    await start(update, context)
#----------------------------------------------------------------------------------------------------------------------Trivia
async def send_trivia_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a trivia question to the user."""
    questionTrivia = random.choice(trivia_questions)
    options = "\n".join([f"- {option}" for option in questionTrivia['options']])
    message = f"{questionTrivia['question']}\n{options}"
    
    # Save the trivia question in the context
    context.user_data['trivia_question'] = questionTrivia

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
#----------------------------------------------------------------------------------------------------------------------lista productos
async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show products to the user."""
    messages = []
    for product in products:
        message = (
            f"*{product['name']}*\n"
            f"{product['description']}\n"
            f"Price: {product['price']}\n"
            f"[Image]({product['image_url']})\n"
            f"Cantidad: {product['cantidad']}\n"
            f"CAD: {product['CAD']}"
        )
        messages.append(message)
    
    for message in messages:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')
#----------------------------------------------------------------------------------------------------------------------Interracion bot
async def interaccion_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Determina si la interacción es un CallbackQuery o un mensaje de texto
    if update.callback_query:
        query = update.callback_query
        pregunta_numero = 1
        context.user_data['pregunta_numero'] = pregunta_numero
        await query.message.reply_text("¿Cuál es tu nombre?")
    elif update.message:
        pregunta_numero = context.user_data.get('pregunta_numero', 1)
        
        if pregunta_numero == 1:
            context.user_data['nombre'] = update.message.text
            await update.message.reply_text(f"Hola {context.user_data['nombre']}.")
            await update.message.reply_text("¿Cuál es tu fecha de nacimiento? (Formato: YYYY-MM-DD)")
            context.user_data['pregunta_numero'] = 2
        elif pregunta_numero == 2:
            try:
                fecha_nacimiento = datetime.datetime.strptime(update.message.text, "%Y-%m-%d").date()
                edad = calcular_edad(fecha_nacimiento)
                context.user_data['edad'] = edad
                await update.message.reply_text(f"Increíble, tienes {edad} años.")
                await update.message.reply_text("¿Cuál es tu color favorito?")
                context.user_data['pregunta_numero'] = 3
            except ValueError:
                await update.message.reply_text("Por favor, ingresa la fecha en el formato correcto: YYYY-MM-DD")
        elif pregunta_numero == 3:
            color_favorito = update.message.text.lower()
            await update.message.reply_text(f"El {color_favorito} es muy bonito, a mí también me gusta.")
            await update.message.reply_text("¿Has utilizado el bot anteriormente?")
            context.user_data['pregunta_numero'] = 4
        elif pregunta_numero == 4:
            respuesta = update.message.text.lower()
            if respuesta == 'si':
                await update.message.reply_text("¡Te agradezco por probar el bot!")
            elif respuesta == 'no':
                await update.message.reply_text("Deberías ver las demás funciones de este bot.")
            await start(update, context)
            context.user_data['pregunta_numero'] = 1
#--------------------------------------------------------------------------------------
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'correct_answer2.1' in context.user_data or 'correct_answer2.2' in context.user_data or 'correct_answer2.3' in context.user_data or 'trivia_question' in context.user_data:
        await answer(update, context)
    else:
        await interaccion_bot(update, context)
#--------------------------------------------------------------------------------------
#Funcion calcular edad
def calcular_edad(fecha_nacimiento):
    hoy = datetime.date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

#Funcion principal
def main():
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CallbackQueryHandler(interaccion_bot, pattern='^2.7$'))

    application.run_polling()
if __name__ == '__main__':
    main()