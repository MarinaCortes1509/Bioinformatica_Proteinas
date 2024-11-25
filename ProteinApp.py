
import streamlit as st  
from Bio.Seq import Seq
from io import StringIO
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Estilos personalizados con Markdown
st.markdown("""
    <style>
    .stSidebar {
        background-color: #000000; /* Fondo negro */
    }
    div[data-testid="stSidebar"] {
        background-color: #000000; /* Fondo negro */
        color: white; /* Texto blanco */
    }
    .title {
        color: #2A9DF4; /* Azul */
        font-family: 'Arial';
        font-size: 36px;
    }
    .subtitle {
        color: #2A9DF4; /* Azul */
        font-family: 'Arial';
        font-size: 20px;
    }
    .highlight {
        background-color: #FFF8DC; 
        padding: 10px;
        border-radius: 5px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar el estado de la aplicación
if "sequence" not in st.session_state:
    st.session_state["sequence"] = None

if "resultados" not in st.session_state:
    st.session_state["resultados"] = StringIO()  # Contenedor para los resultados

# Opciones del menú
st.sidebar.header("Menú Principal")
menu_option = st.sidebar.selectbox(
    "Seleccione una opción:",
    ["Inicio", "Cargar Secuencia", "Procesar Secuencia", "Visualizar Proteína en 3D", "Descargar Resultados"]
)

if menu_option == "Inicio":
    # Mostrar el título y la imagen solo en la pestaña de inicio
    st.markdown("<h1 class='title'>Procesos Fundamentales de Expresión Génica y Síntesis de Proteínas</h1>", unsafe_allow_html=True)
    st.image("C:/Users/marin/codigo/app_proteins/py/imagen proteina/pixelcut-export.png", use_container_width=True)
    
    st.markdown("""
        ### Introducción a la Aplicación

Bienvenido a nuestra aplicación interactiva diseñada para explorar y analizar secuencias genéticas. Con esta herramienta, podrás realizar diversas operaciones fundamentales en la biología molecular, como:

- Visualizar la longitud de una secuencia genética.
- Realizar procesos de transcripción y traducción para comprender cómo se forman las proteínas.
- Visualizar modelos de proteínas en 3D.
- Descargar los resultados del análisis para un uso más amplio.

**¿Qué son las proteínas y por qué son importantes?**  
Las proteínas son macromoléculas formadas por cadenas de aminoácidos unidos por enlaces peptídicos, cuya secuencia está determinada por el material genético. Se caracterizan por tener estructuras organizadas en niveles (primaria, secundaria, terciaria y cuaternaria), que les confieren propiedades únicas. Cumplen diversas funciones en el organismo: estructurales (colágeno), enzimáticas (catalizadores), de transporte (hemoglobina), reguladoras (hormonas), defensivas (anticuerpos) y energéticas (como fuente de energía en casos extremos).

**Transcripción y Traducción**  
- **Transcripción**: Es el proceso en el cual la información genética de una secuencia de ADN se copia a una molécula de ARN mensajero (ARNm). Esto ocurre en el núcleo y está mediado por la enzima ARN polimerasa.
- **Traducción**: Posteriormente, el ARNm se transporta al citoplasma para la traducción, donde la secuencia de nucleótidos del ARNm se convierte en una secuencia de aminoácidos para formar una proteína. Este proceso se realiza en los ribosomas, con la ayuda del ARN de transferencia (ARNt), que lleva los aminoácidos específicos según el código genético.

Además, esta aplicación incluye una funcionalidad para visualizar proteínas en 3D, permitiéndote observar su estructura tridimensional, y la posibilidad de descargar todos los resultados obtenidos para tu análisis. ¡Explora y experimenta con el fascinante mundo de las proteínas!
    """)

elif menu_option == "Cargar Secuencia":
    st.markdown("<h2 class='subtitle'>Cargar una Secuencia</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Sube un archivo con una secuencia (formato FASTA o texto)", type=["txt", "fasta"])

    if uploaded_file:
        # Leer el archivo cargado
        content = uploaded_file.getvalue().decode("utf-8")
        st.text_area("Contenido del archivo:", content, height=200)

        # Guardar la secuencia cargada en una variable
        sequence = "".join(content.splitlines()[1:])  # Ignorar la línea de encabezado en FASTA
        st.session_state["sequence"] = sequence  # Guardar en la sesión
        st.success("✅ Secuencia cargada con éxito.")

elif menu_option == "Procesar Secuencia":
    st.subheader("Procesar la Secuencia Cargada")

    if st.session_state["sequence"]:
        sequence = st.session_state["sequence"]
        st.write(f"Secuencia actual: `{sequence}`")

        # Crear un objeto Seq
        bio_seq = Seq(sequence)

        # Mostrar análisis básico
        st.write("**Resultados del análisis:**")
        st.write(f"- Longitud: {len(bio_seq)}")
        st.write(f"- Complementaria: {bio_seq.complement()}")
        st.write(f"- Transcrita: {bio_seq.transcribe()}")

        # Verificar si la longitud es divisible por 3
        if len(bio_seq) % 3 != 0:
            st.warning("⚠️ La longitud de la secuencia no es múltiplo de 3. La traducción podría no ser correcta.")

        # Intentar traducir la secuencia
        try:
            translated = bio_seq.translate(to_stop=True)
            st.write(f"- Traducida: {translated}")
        except Exception as e:
            st.error(f"⚠️ Error durante la traducción: {str(e)}")
            translated = "Error en la traducción"

        # Escribir resultados en el contenedor del estado
        st.session_state["resultados"] = StringIO()  # Reiniciar
        resultados = st.session_state["resultados"]
        resultados.write("Resultados del análisis de la secuencia:\n")
        resultados.write(f"Secuencia original: {sequence}\n")
        resultados.write(f"Longitud: {len(bio_seq)}\n")
        resultados.write(f"Complementaria: {bio_seq.complement()}\n")
        resultados.write(f"Transcrita: {bio_seq.transcribe()}\n")
        resultados.write(f"Traducida: {translated}\n")
    else:
        st.error("⚠️ Primero debes cargar una secuencia en la sección anterior.")

elif menu_option == "Visualizar Proteína en 3D":
    st.markdown("<h2 class='subtitle'>Visualizar una proteína en 3D</h2>", unsafe_allow_html=True)

    # Subir un archivo PDB
    pdb_file = st.file_uploader("Sube un archivo en formato PDB", type=["pdb"])

    if pdb_file:
        pdb_content = pdb_file.getvalue().decode("utf-8")

        # Parsear las coordenadas de átomos desde el archivo PDB
        atom_coordinates = []
        for line in pdb_content.splitlines():
            if line.startswith("ATOM"):  # Buscar líneas que contengan átomos
                x = float(line[30:38].strip())  # Coordenada X
                y = float(line[38:46].strip())  # Coordenada Y
                z = float(line[46:54].strip())  # Coordenada Z
                atom_coordinates.append((x, y, z))

        # Separar las coordenadas en listas
        xs, ys, zs = zip(*atom_coordinates)

        # Visualizar en 3D usando Matplotlib
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(xs, ys, zs, c="b", marker="o")
        ax.set_title("Visualización de la proteína en 3D")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        st.pyplot(fig)

        st.success("✅ Visualización completada.")
    else:
        st.warning("⚠️ Por favor, sube un archivo PDB para continuar.")

elif menu_option == "Descargar Resultados":
    st.markdown("<h2 class='subtitle'>Descargar Resultados del Análisis</h2>", unsafe_allow_html=True)

    if st.session_state["resultados"].getvalue():  # Verificar si hay contenido en resultados
        st.download_button(
            label="Descargar resultados",
            data=st.session_state["resultados"].getvalue(),
            file_name="resultados_analisis.txt",
            mime="text/plain"
        )
    else:
        st.error("⚠️ No hay resultados disponibles para descargar.")
