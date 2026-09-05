import discord
from model import predict
from discord.ext import commands 


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = "/", intents = intents)

@bot.event 
async def on_ready():
    print("bot en linea ve a discord")

@bot.event
async def on_member_join(member):
    print(f"{member} se ha unido al servidor")


@bot.command()
async def check(ctx):
    await ctx.send("Ingresa una imagen para analizarla.")

    def verificar_imagen(mensaje):
        return mensaje.author == ctx.author and len(mensaje.attachments)>0

    try:
        mensaje =await bot.wait_for("message", check =verificar_imagen, timeout=60)
        contenido = mensaje.attachments[0]
        await contenido.save(f"img/{contenido.filename}")
        await ctx.send("Imagen recibida y guardada correctamente.")
        resultado = predict(image_path = f"img/{contenido.filename}",model_path = "keras_model.h5",labels_path = "labels.txt")
        await ctx.send(resultado)
    except ValueError as e:
        await ctx.send("No se recibio imagen o se excedio el tiempo de espera.")


bot.run()