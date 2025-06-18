import asyncio
import edge_tts

async def text_to_audio(text):
    communicate = edge_tts.Communicate(text, voice="es-MX-DaliaNeural")
    await communicate.save("salida.mp3")

asyncio.run(text_to_audio("El inventario de mercadería, en términos simples, es la lista detallada de todos los productos que una empresa tiene en su poder para vender o para utilizar en su producción. Es una herramienta esencial para el control del stock, la gestión de ventas y la planificación de compras. "))
