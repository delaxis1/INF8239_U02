# Conclusión · Ejercicio 03

**INF-8239 Ciencia de Datos II · Unidad 02** · Alexis De La Cruz · 100805370

<!-- inicio -->
Quería saber si un clasificador entrenado solo con el texto de un SMS puede separar el spam de los
mensajes legítimos, y a qué costo en mensajes legítimos bloqueados. El corpus es SMS Spam Collection
de UCI: 5 574 mensajes en inglés, 13.4 % de spam.

La auditoría encontró 414 textos duplicados, un 7.4 %. Los eliminé antes de particionar, porque un
mensaje repetido a ambos lados del corte haría que el modelo acertara por haberlo memorizado.
Quedaron 5 160 mensajes: 3 870 para entrenar y 1 290 para medir, con 160 spam. La línea base, que
responde "ham" a todo, obtiene 88 % de exactitud y 0.467 de F1 macro. Es la misma trampa de la
unidad anterior: un modelo inútil con una exactitud presentable.

La regresión logística alcanzó 0.956 de F1 macro y Naive Bayes 0.933. Si la decisión terminara ahí,
elegiría la logística. Pero las dos se equivocan de forma distinta, y en este problema los errores
no cuestan lo mismo. La logística bloquea 15 mensajes legítimos y deja pasar 10 spam; Naive Bayes
bloquea 5 y deja pasar 30. Pasar de uno a otro significa bloquear 10 mensajes reales más para
detener 20 anuncios más: un mensaje de una persona perdido por cada dos spam atrapados. Si un SMS
legítimo que nunca llega vale más que dos spam que sí llegan —y un aviso de trabajo o de un familiar
lo vale—, la elección correcta es Naive Bayes, aunque su F1 macro sea menor. La métrica principal
ordena los modelos; el costo del error decide.

La clase difícil es el spam en ambos modelos: su recall es 0.938 en la logística y 0.812 en Naive
Bayes, frente a 0.987 y 0.996 de los mensajes legítimos. Era previsible con 13.4 % de ejemplos.

Leí los 25 errores de la logística uno por uno. Entre los 15 falsos positivos, 6 reutilizan
vocabulario de spam —"free", "call", "offer"— y 5 son simplemente demasiado cortos: "I'm at work.
Please call" tiene cinco palabras y ninguna distingue a una persona de una campaña. Entre los 10
falsos negativos, 6 son spam conversacional, escrito como un mensaje personal, sin números cortos ni
mayúsculas: "Sorry I missed your call let's talk when you have the time". El modelo aprendió la
forma del spam de 2012, no su intención, y ese es el error más frecuente y el más difícil de
corregir con TF-IDF, que solo ve palabras sueltas y pares.

Cuatro de los 25 tienen etiqueta discutible en el corpus original. Parte del techo no es del modelo.

La limitación mayor es la población: inglés, año 2012, estudiantes de Singapur y un foro británico.
Nada de eso representa los SMS que recibe hoy una persona en República Dominicana, así que el
resultado no debe leerse como una medida de lo que lograría un filtro actual.

Antes de desplegarlo haría tres cosas. Fijar el umbral de decisión a partir del costo real de
bloquear un mensaje legítimo, en vez de aceptar el 0.5 por defecto. Validar con mensajes recientes y
en el idioma de destino. Y mostrar siempre la predicción como lo que es, una sugerencia con un
margen de error conocido, nunca como una verdad sobre el mensaje.
<!-- fin -->
