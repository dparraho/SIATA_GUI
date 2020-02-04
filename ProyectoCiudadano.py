# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 2019

@author: Daniel Parra
"""

from tkinter import Label, Button, Toplevel, StringVar, IntVar, Entry, Tk, CENTER, messagebox, ttk, PhotoImage, Canvas
import webbrowser
from pandas import read_csv
from urllib.request import urlopen
import numpy as np
import matplotlib
import paramiko
from glob import glob
from os import mkdir
from ast import literal_eval
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from PIL import ImageTk, Image
from pdf2image import convert_from_path
matplotlib.use('TkAgg')
# import time
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
#import pypdfocr.pypdfocr_gs as pdfImg
#from PIL import Image, ImageTk

ventana = Tk()
ventana.title("ProyectoCiudadanosCientificos")
ventana.geometry("1000x600")

# Creando las pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand='yes')

# pestaña
pes0 = ttk.Frame(notebook)  # pestaña # 1
notebook.add(pes0, text='Aire')
pes1 = ttk.Frame(notebook)  # pestaña # 2
notebook.add(pes1, text='Graficacion')

background_image = Image.open('SIATA.jpg')
ancho = 1000
wpercent = (ancho / float(background_image.size[0]))
hsize = int((float(background_image.size[1]) * float(wpercent)))
background_image = background_image.resize((ancho, hsize), Image.ANTIALIAS)
background_image = ImageTk.PhotoImage(background_image)
background_label = Label(pes0, image=background_image, compound=CENTER)
background_label.place(x=0, y=0, relwidth=1, relheight=1)



nube = IntVar()
nube.set(185)
estacion = ttk.Combobox(pes0, width=12, state="readonly")
variable = ttk.Combobox(pes0, width=12, state="readonly")
EstMeteoInterna = ttk.Combobox(pes1, width=12, state="readonly")
MeteoInternaVariable = ttk.Combobox(pes1, width=18, state="readonly")
variable2 = ttk.Combobox(pes1, width=12, state="readonly")
varsDescargar = ttk.Combobox(pes0, width=12, state="readonly")
MainVars = ttk.Combobox(pes0, width=12, state="readonly")
files_variable = ttk.Combobox(pes0, width=50, state="readonly")
cuadrito = ttk.Combobox(pes0, width=50, state="readonly")
ano = ttk.Combobox(pes0, width=12, state="readonly")
conteo = ttk.Combobox(pes0, width=50, state="readonly")
barras = ttk.Combobox(pes0, width=50, state="readonly")
varsNubes = ttk.Combobox(pes0, width=20, state="readonly")
descarga = StringVar()
descarga.set('Descargas/')
fileDescarga = StringVar()
fileDescarga.set('Datos.csv')
var = None
FechaiNube = StringVar()
FechaiNube.set((datetime.now() - relativedelta(days=20)).strftime('%Y-%m-%d'))
FechafNube = StringVar()
FechafNube.set((datetime.now()).strftime('%Y-%m-%d'))
FechaiDatos = StringVar()
FechafDatos = StringVar()
Nubes = StringVar()
TextsaveNubes = StringVar()
TextsaveNubes.set('Temporal')
Textsavegraph = StringVar()
filtro1 = StringVar()
filtro1.set(250)
filtro2 = StringVar()
filtro2.set(250)
check_df = IntVar()
check_df.set(0)
send = StringVar()
dicc_positions = {}
FechaiMeteo = StringVar()
FechaiMeteo.set((datetime.now() - relativedelta(days=4)).strftime('%Y-%m-01 01:00'))
FechafMeteo = StringVar()
FechafMeteo.set((datetime.now()).strftime('%Y-%m-%d 00:00'))
#progress = ttk.Progressbar(pes0, orient="horizontal", length=200, mode="determinate")
#progress["value"] = 0
#progress["maximum"] = 960
#progress.place(x=780, y=550)
password = StringVar()

places = {'files_variable':[120, 130],'descargar_variable':[450, 130],'files_cuadrito':[120, 280],'descargar_cuadrito':[450, 280],
'consultar_cuadrito':[30, 230],'ano_cuadrito':[120, 240],'files_conteo':[120, 343],'descargar_conteo':[450, 340],
'consultar_conteo':[30, 330],'files_barras':[120, 393],'descargar_barras':[450, 390],'consultar_barras':[30, 380],
'box_password':[120, 30],'label_password':[30, 30],'textsave_nubes':[685, 280],'box_nubes':[840, 230],
'label_nubes':[840, 208],'box_fechai_nubes':[685, 102],'label_fechai_nubes':[680, 80],'box_fechaf_nubes':[755, 102],
'label_fechaf_nubes':[755, 80],'variables_nubes':[685, 230],'display_variables_nubes':[850, 252],
'boton_add':[685, 252],'boton_remove':[720, 252],'box_filtro_nova':[685, 152],'label_filtro_nova':[680, 130],
'box_filtro2_nova':[755, 152],'label_filtro2_nova':[755, 130],'filtro_df':[685, 182],'mensaje_calibro':[840, 252],
'calibrar_nube':[600, 130],'caja_nube':[685, 40],'boton_estado':[750, 35],'boton_calibracion':[810, 35],
'espectrometro':[30, 600],'descargar_nubes':[600, 230],'box_fechai_meteo':[685, 350],'label_fechai_meteo':[680, 328],
'box_fechaf_meteo':[785, 350],'label_fechaf_meteo':[785, 328],'descargar_red':[30, 430],'box_fechai_red':[105, 452],
'label_fechai_red':[100, 430],'box_fechaf_red':[175, 452],'label_fechaf_red':[175, 430],'variables_red':[250, 452],
'textsave_red':[355, 452],'label_internas':[580, 310],'actualizar_internas':[600, 350],'mostrar_temperatura':[600, 400],
'mostrar_humedad':[680, 400], 'variable_para_consultar':[120, 90], 'estacion_para_consultar':[220, 90],
'textsave_consulta':[325, 92],'consultar_variable':[30, 80]
          }

places2 = {'estaciones_internas':[150, 275],'temperatura_o_humedad':[10, 275],'texto_internas':[20, 100],
'invalidar_internas':[60, 175],'validar_internas':[10, 175],'validar_una_interna':[250, 265],'color_variable':[80, 70],
'label_color_variable':[20, 70],'label_archivo_enviar':[20, 20],'box_archivo_enviar':[80, 20],'hacer_serie':[250, 20],
'hacer_histograma':[300, 20],'hacer_histograma_ICA':[380, 20],'label_textsave_figuras':[20, 45],'box_textsave_figuras':[80, 45],
'box_fechai_meteo':[120, 198],'label_fechai_meteo':[120, 170],'box_fechaf_meteo':[220, 198],'label_fechaf_meteo':[220, 170]
           }

_ = read_csv('Ubicaciones_ubuntu.csv', header=[0, 1], index_col=0)
places = _['pes0']
places2 = _['pes1']
def send_copy(file, endswith='SAL-9000', specific_folder=''):#
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(r'siata.gov.co', username='dparraho', password=password.get(), port=22,timeout=4)
    buff = ''
    sftp = ssh.open_sftp()
    sftp.put(file, r'Temporal/%s' % file)
    chan = ssh.invoke_shell()
    print('scp ' + 'Temporal/%s' % file + ' dparraho@gomita:/home/calidadaire/JupyterNotebooks/dparraho/Temporal/%s \n' % specific_folder)
    chan.send('cp ' + 'Temporal/%s' % file + ' /var/www/CalidadAire/AnalisisDatos/Daniel/from_app%s/ \n' % specific_folder)
    chan.send('scp ' + 'Temporal/%s' % file + ' dparraho@gomita:/home/calidadaire/JupyterNotebooks/dparraho/Temporal/%s \n' % specific_folder)
    while not buff.endswith('password: '):
        resp = chan.recv(9999)
        buff += resp.decode("utf-8")
        #print(buff)
    print('Enviando contraseña')
    chan.send('%s\n'%password.get())
    buff=''
    while not endswith in buff:
        resp = chan.recv(9999)
        buff += resp.decode("utf-8")
        #print(buff)
    print('Closing conection...')
    ssh.close()

class crear:
    '''Esta clase es con el propósito de facilitar la edición de los parámetros en cajas,
    labels, etc.'''
    def __init__(self, pes):
        self.pes = pes

    def caja(self, TextV, Width, x, y):  # (Variable, espesor, posición x, posición y)
        self.refcaja = Entry(self.pes, textvariable=TextV, width=Width).place(x=x, y=y)

    def label(self, Text, x, y, **kwargs):
        self.foreground = kwargs.get('foreground', 'black')
        self.background = kwargs.get('bg', 'white')
        self.idxlabel = Label(self.pes, text=Text, foreground=self.foreground, bg=self.background).place(x=x, y=y)

    def boton(self, Text, comando, x, y, bg="#9ACD32", fg="black"):
        boton = Button(self.pes, text=Text, command=comando, bg=bg, fg=fg).place(x=x, y=y)

    def botonC(self, Text, TextV, x, y):
        botonC = ttk.Checkbutton(self.pes, text=Text, variable=TextV).place(x=x, y=y)

def sshconsulta(link, folder=None, local_var=None):
    global var
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    var = 'PM25' if variable.get()=='PM2.5' else 'PM25M' if variable.get()=='PM2.5M' else 'Rosas_Bivariadas' if variable.get()=='Rosas Bivariadas'  else variable.get()
    ssh.connect(r'siata.gov.co', username='dparraho', password=password.get(), port=22)
    print('SAL directory %s%s'%(link, var if folder is None else folder))
    ssh_stdin, ssh_stout, ssh_stderr = ssh.exec_command('cd %s%s \n ls -l'%(link, var if folder is None else folder))

    print('ssh succesfull. Closing connection')
    try:
        ssh_stout = ssh_stout.readlines()
        ssh_stout = [i.encode("utf-8").decode().strip('\n') for i in ssh_stout]
        ssh_stout = [[ssh_stout[i].split()[-4:]] for i in range(1, len(ssh_stout))]
        ssh_stout = [[' '.join(i[0][:3]), i[0][-1]] for i in ssh_stout]
        ssh_stout = np.array(ssh_stout)

        if 'Daniel' in link or 'conteo' in link or local_var is not None:
            mask = [(local_var in i[-1]) for i in ssh_stout]
            ssh_stout = ssh_stout[mask]
        elif not 'Espectrometro' in link and not 'Cuadritos' in link and not 'Barras' in link and not 'Daniel' in link:
            mask = [(estacion.get() in i[-1]) for i in ssh_stout]
            ssh_stout = ssh_stout[mask]
        elif 'Cuadritos' in link and not 'Daniel' in link:
            mask = [(ano.get() in i[-1]) for i in ssh_stout]
            ssh_stout = ssh_stout[mask]

        files = ssh_stout[:, 1]
        ssh_stout = [('['+i[0]+']'+' '+i[1]) for i in ssh_stout]
        ssh.close()
    except:
        print('Fallo')
        ssh_stout = []
        ssh.close()
    print('Connection closed')

    return ssh_stout, files

############################## ESTACION ################################3
def consultarEstacion():
    ssh_stout, _ = (sshconsulta('/var/www/CalidadAire/Figuras/') if 'Minutales' not in variable.get() and 'Rosas' not in variable.get()
                 else sshconsulta('/var/www/CalidadAire/PM25_Minutales/', folder='') if 'Rosas' not in variable.get()
                    else sshconsulta('/var/www/CalidadAire/Rosas_Bivariadas/', folder=''))
    if not ssh_stout:
        files_variable.set('')
    files_variable['values'] = sorted(ssh_stout)
    files_variable.place(x=places['files_variable'][0], y=places['files_variable'][1])
    files_variable.current(0)
    botonDescargar = Button(pes0, text="Descargar", command=descargarEstacion, bg="yellow",
                            fg="black").place(x=places['descargar_variable'][0], y=places['descargar_variable'][1])

def descargarEstacion():
    grafica = (urlopen('http://siata.gov.co/CalidadAire/Figuras/%s/%s' % (var, files_variable.get().split()[-1]))
               if not any(x in variable.get() for x in ['Rosas', 'Minutales']) else
               urlopen('http://siata.gov.co/CalidadAire/PM25_Minutales/%s' % files_variable.get().split()[-1])
               if 'Rosas' not in variable.get()
               else urlopen('http://siata.gov.co/CalidadAire/Rosas_Bivariadas/%s' % files_variable.get().split()[-1]))
    try:
        file = open('%s%s' % (descarga.get(), files_variable.get().split()[-1]), 'wb'); file.write(grafica.read()); file.close()
    except FileNotFoundError:
        mkdir(descarga.get())
        file = open('%s%s' % (descarga.get(), files_variable.get().split()[-1]), 'wb'); file.write(grafica.read()); file.close()
    popup_bonus('%s%s' % (descarga.get(), files_variable.get().split()[-1]), '%s' % files_variable.get().split()[-1], 1000)
    print('---------------------------------------------------------------------------------------------------------')
    print('ARCHIVO %s EXITOSAMENTE DESCARGADO :D' % files_variable.get().split()[-1])
    print('---------------------------------------------------------------------------------------------------------')

############################### ESPECTROMETRO ################################
def espectrometro():
    ssh_stout, _ = sshconsulta('/var/www/CalidadAire/Espectrometro/', folder='')
    for archive in ssh_stout:
        grafica = urlopen('http://siata.gov.co/CalidadAire/Espectrometro/%s'%archive.split()[-1])
        file = open('Espectrometro/%s'%archive.split()[-1], 'wb');
        file.write(grafica.read());
        file.close()

############################### CUADRITOS ####################################
def consultarCuadritos():
    ssh_stout, _ = sshconsulta('/var/www/CalidadAire/Figuras/PM25/Historicos/Cuadritos/', folder='')
    if not ssh_stout:
        cuadrito.set('')
    cuadrito['values'] = (ssh_stout)
    cuadrito.place(x=places['files_cuadrito'][0], y=places['files_cuadrito'][1])
    cuadrito.current(0)

    name_file = cuadrito.get().split()[-1]
    path = 'http://siata.gov.co/CalidadAire/Figuras/PM25/Historicos/Cuadritos/%s' % name_file
    folder = 'Cuadritos/'
    botonCuadritos = Button(pes0, text="Descargar", command=lambda: descarga_un_archivo(path, folder, name_file),
                            bg="yellow", fg="black").place(x=places['descargar_cuadrito'][0], y=places['descargar_cuadrito'][1])

def descarga_un_archivo(path, folder, name_file, width=1000, title='NA'):
    grafica = urlopen(path)
    file = open('%s%s' % (folder, name_file), 'wb'); file.write(grafica.read()); file.close()

    print('---------------------------------------------------------------------------------------------------------')
    print('ARCHIVO %s EXITOSAMENTE DESCARGADO :D' % name_file)
    print('---------------------------------------------------------------------------------------------------------')
    popup_bonus('%s%s' % (folder, name_file), title, width)


botonCuadritos = Button(pes0, text="Consultar\nCuadritos", command=consultarCuadritos, bg="#009",
                       fg="white").place(x=places['consultar_cuadrito'][0], y=places['consultar_cuadrito'][1])

ano['values'] = ['', 2014, 2015, 2016, 2017, 2018, 2019]
ano.place(x=places['ano_cuadrito'][0], y=places['ano_cuadrito'][1])
ano.current(0)

################################ CONTEO ICA ##############################################
def callback(url):
    webbrowser.open_new(url)

def multiple_popup(title, screen_h, screen_v, divisor_h, ListaArchivos, pos, links, local_folder=''):
    global basewidth, hsize, pop_up_x, pop_up_y, img, win
    try:
        win.destroy()
    except:
        pass
    win = Toplevel()
    win.wm_title(title)
    win.geometry("%dx%d" % (screen_h, screen_v))
    for idx, i in enumerate(ListaArchivos):
        pop_up_x = pos[idx][1]
        pop_up_y = pos[idx][0]
        try:
            img = Image.open('%s%s' % (local_folder, i))
            basewidth = int(screen_h / divisor_h * 1.1)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        except OSError:
            img, basewidth, hsize = PDF_to_JPG('%s%s' % (local_folder, i), int(screen_h / divisor_h))
        a = exec('global my_img%s; my_img%s = ImageTk.PhotoImage(img)' % (idx, idx))
        b = exec('my_label%s = Label(win, image=my_img%s)' % (idx, idx))
        c = exec('my_label%s.place(x=pop_up_x, y=pop_up_y)' % idx)
        d = exec('my_label%s.bind("<Button-1>", lambda e: callback("%s"))' % (idx, links[idx]))

def consultarConteo():
    global basewidth, hsize, pop_up_x, pop_up_y, img, win, progress
    path = '/var/www/CalidadAire/Figuras/PM25/ICA_conteo/'
    ssh_stout, ListaArchivos = sshconsulta(path, folder='', local_var='Conteo')
    if not ssh_stout:
        conteo.set('')
    conteo['values'] = ssh_stout
    conteo.place(x=places['files_conteo'][0], y=places['files_conteo'][1])
    conteo.current(0)

    links = []
    for i in ListaArchivos:
        links.append('http://siata.gov.co/%s/%s' % (path.strip('/var/www/'), i))
        graficaestado = urlopen(
            'http://siata.gov.co/%s/%s' % (path.strip('/var/www/'), i))
        file = open('Conteo/%s'%i, 'wb'); file.write(graficaestado.read()); file.close()

    screen_h = int(1366)
    screen_v = 768
    divisor_h = 5
    divisor_v = 5.4
    pos = [(0, i) for i in range(0, screen_h - 1, int(screen_h / divisor_h))] \
          + [(int(screen_v / divisor_v), i) for i in range(0, screen_h - 1, int(screen_h / divisor_h))] \
          + [(int(screen_v / divisor_v) * 2, i) for i in range(0, screen_h - 1, int(screen_h / divisor_h))] \
          + [(int(screen_v / divisor_v) * 3, i) for i in range(0, screen_h - 1, int(screen_h / divisor_h))] \
          + [(int(screen_v / divisor_v) * 4, i) for i in range(0, screen_h - 1, int(screen_h / divisor_h))]
    multiple_popup('Gráficas conteo', screen_h, screen_v, divisor_h, ListaArchivos, pos, links, 'Conteo/')


    name_file = conteo.get().split()[-1]
    path = 'http://siata.gov.co/CalidadAire/Figuras/PM25/ICA_conteo/%s' % name_file
    folder = 'Conteo/'
    botonCuadritos = Button(pes0, text="Descargar", command=lambda: descarga_un_archivo(path, folder, name_file), bg="yellow",
                            fg="black").place(x=places['descargar_conteo'][0], y=places['descargar_conteo'][1])

botonConteo = Button(pes0, text="Consultar\nConteo", command=consultarConteo, bg="#009",
                       fg="white").place(x=places['consultar_conteo'][0], y=places['consultar_conteo'][1])

################################ BARRAS ##############################################
def consultarBarras():
    ssh_stout, _ = sshconsulta('/var/www/CalidadAire/Figuras/PM25/Historicos/Barras/', folder='')
    if not ssh_stout:
        barras.set('')
    barras['values'] = ssh_stout
    barras.place(x=places['files_barras'][0], y=places['files_barras'][1])
    barras.current(0)

    name_file = barras.get().split()[-1]
    path = 'http://siata.gov.co/CalidadAire/Figuras/PM25/Historicos/Barras/%s' % name_file
    folder = 'Barras/'
    botonCuadritos = Button(pes0, text="Descargar", command=lambda: descarga_un_archivo(path, folder, name_file), bg="yellow",
                            fg="black").place(x=places['descargar_barras'][0], y=places['descargar_barras'][1])

botonConteo = Button(pes0, text="Consultar\nBarras", command=consultarBarras, bg="#009",
                       fg="white").place(x=places['consultar_barras'][0], y=places['consultar_barras'][1])

def selection(event=None):
    estacion['values'] = dict_vars[variable.get()]
    estacion.current(len(estacion['values'])-1)

################################# Descarga Datos Nube ##########################################
def datosNube():
    FechaiNube.set((datetime.now() - relativedelta(days=1)).strftime('%Y-%m-%d') if FechafNube.get() == ''
                   else FechaiNube.get())
    FechafNube.set((datetime.now()).strftime('%Y-%m-%d') if FechafNube.get() == '' else FechafNube.get())
    file = 'sudo su - ciudadanos_cientificos\n cd modulo_ciudadanos\n cd tempDaniel'
    command = 'python DatosDaniel.py "%s" "%s" "%s" "%s" "%s"\n' % (FechaiNube.get(), FechafNube.get(),
                                                                    list(literal_eval('[' + Nubes.get() + ']')),
                                                                    [DiccionarioVariablesNubes[i] for i in
                                                                     ListaVarsNubes],
                                                                    TextsaveNubes.get())
    endswith = 'ciudadanos_cientificos@gomita:~/modulo_ciudadanos/tempDaniel$ '
    file_a_guardar = '%s_%s.csv' % (TextsaveNubes.get(), [DiccionarioVariablesNubes[i] for i in ListaVarsNubes][0])
    comando_a_gomita(file, command, endswith, file_a_guardar=file_a_guardar, specific_file='datos_nubes/')

def comando_a_gomita(file, command, endswith,file_a_guardar=None,specific_file=''):
    """
    :param file: strign object that could including -sudo su- command, followed by a -\n- and ending with a -cd- command
    :param command: usually - python script.py - command with its arguments
    :param endswith: afterwards changing to the interested folder, the terminal will have an output that usually looks
                    like ciudadanos_cientificos@gomita:~/folder/$ this have to be specified in endswith
    :param file_a_guardar: a scp command will be execute with this param diferent to None
    :param specific_file: specifici file inside .../AnalisisDatos/Daniel/ www folder
    :return:
    """
    global progress
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(r'siata.gov.co', username='dparraho', password=password.get(), port=22)

    try:
        chan = ssh.invoke_shell()
        print('Shell Invocado')
        chan.send('ssh dparraho@gomita\n')
        buff = ''
        while not buff.endswith('dparraho@gomita\'s password: '):
            resp = chan.recv(9999)
            buff += resp.decode("utf-8")

        # Send the password and wait for a prompt.
        chan.send('%s\n'%password.get())
        buff = ''
        while not buff.endswith('dparraho@gomita:~$ '):
            resp = chan.recv(9999)
            buff += resp.decode("utf-8")
        print('Entró a gomita')

        chan.send('%s\n %s\n' % (file, command))
        print(command)

        buff = ''
        c = 0
        bytes = 10
        while not buff.endswith(endswith):
            resp = chan.recv(9999)
            buff += resp.decode("utf-8")
            bytes += 10
            #progress["value"] = bytes
        print(buff)
        print('Ejecutó el comando')

        if file_a_guardar is not None:
            print('scp ' + file_a_guardar + ' dparraho@siata.gov.co:/var/www/CalidadAire/AnalisisDatos/Daniel/%s \n'%specific_file)
            chan.send('scp ' + file_a_guardar + ' dparraho@siata.gov.co:/var/www/CalidadAire/AnalisisDatos/Daniel/%s \n'%specific_file)
            while not buff.endswith('Password: '):
                resp = chan.recv(9999)
                buff += resp.decode("utf-8")
            print(buff)
            chan.send('%s\n'%password.get())
            while not buff.endswith(endswith):
                resp = chan.recv(9999)
                buff += resp.decode("utf-8")
        # Now buff has the data I need

    except:
        print('Fail')
        ssh.close()
    ssh.close()
    print('Connection closed')
    try:
        return buff
    except:
        False

globalC = 0

idx_password = Entry(pes0,textvariable=password, show="*", width=15).place(x=places['box_password'][0], y=places['box_password'][1])
idx_password = crear(pes0)
idx_password.label('Password', places['label_password'][0], places['label_password'][1])

idx_textsave = crear(pes0)
idx_textsave.caja(TextsaveNubes, 15, places['textsave_nubes'][0], places['textsave_nubes'][1])

idx_Nubes = crear(pes0)
idx_Nubes.caja(Nubes, 20, places['box_nubes'][0], places['box_nubes'][1])
idx_Nubes.label('Nubes', places['label_nubes'][0], places['label_nubes'][1])

idx_fechai = crear(pes0)
idx_fechai.caja(FechaiNube, 10, places['box_fechai_nubes'][0], places['box_fechai_nubes'][1])
idx_fechai.label('Fecha inicial', places['label_fechai_nubes'][0], places['label_fechai_nubes'][1])

idx_fechaf = crear(pes0)
idx_fechaf.caja(FechafNube, 10, places['box_fechaf_nubes'][0], places['box_fechaf_nubes'][1])
idx_fechaf.label('Fecha final', places['label_fechaf_nubes'][0], places['label_fechaf_nubes'][1])
DiccionarioVariablesNubes = {"PM2.5 DF":"pm25_df","PM2.5 NOVA":"pm25_nova", "PM10 DF":"pm10_df",
                             "PM10 NOVA":"pm10_nova", "Temperatura":"temperatura",
                             "Humedad Relativa":'humedad_relativa'}
varsNubes['values'] = list(DiccionarioVariablesNubes.keys())
varsNubes.place(x=places['variables_nubes'][0], y=places['variables_nubes'][1])
varsNubes.current(globalC)
ListaVarsNubes = []

def aux_label():
    global ListaVarsNubes, idx_escogido
    try:
        idx_escogido.destroy()
    except:pass
    idx_escogido = Label(pes0, text=' \n'.join(ListaVarsNubes), anchor="e")
    idx_escogido.place(x=places['display_variables_nubes'][0], y=places['display_variables_nubes'][1])

def addNubes():
    global ListaVarsNubes, idx_escogido, globalC
    if varsNubes.get() not in ListaVarsNubes:
        ListaVarsNubes.append(varsNubes.get())
    aux_label()
    globalC += 1
    if globalC < 6:
        varsNubes.current(globalC)
    else:
        globalC = 0
        varsNubes.current(globalC)

def removeNubes():
    global ListaVarsNubes, idx_escogido, globalC
    if varsNubes.get() in ListaVarsNubes:
        ListaVarsNubes.remove(varsNubes.get())
    aux_label()
    globalC += 1
    if globalC < 6:
        varsNubes.current(globalC)
    else:
        globalC = 0
        varsNubes.current(globalC)

botonAdd = Button(pes0, text="Add", command=addNubes, bg="#004",
                       fg="white").place(x=places['boton_add'][0], y=places['boton_add'][1])
botonRemove = Button(pes0, text="Remove", command=removeNubes, bg="gray",
                       fg="white").place(x=places['boton_remove'][0], y=places['boton_remove'][1])

################################### CALIBRAR NUBE ##############################################
idx_filtro1 = crear(pes0)
idx_filtro1.caja(filtro1, 10, places['box_filtro_nova'][0], places['box_filtro_nova'][1])
idx_filtro1.label('Filtro PM2.5',  places['label_filtro_nova'][0], places['label_filtro_nova'][1], bg=None)

idx_filtro2 = crear(pes0)
idx_filtro2.caja(filtro2, 10, places['box_filtro2_nova'][0], places['box_filtro2_nova'][1])
idx_filtro2.label('Filtro PM10', places['label_filtro2_nova'][0], places['label_filtro2_nova'][1])

idx_filtrodf = crear(pes0)
idx_filtrodf.botonC('Filtro DF', check_df,  places['filtro_df'][0], places['filtro_df'][1])

def Open_PNG(file, width):
    img = Image.open(file)
    basewidth = int(width)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    return img, basewidth, hsize

def popup_bonus(file, title, width):
    global win, img, my_img, win, pop_up_x, pop_up_y, basewidth, hsize
    pop_up_x = 0
    pop_up_y = 0
    print(file)
    img, basewidth, hsize = PDF_to_JPG(file, width) if not any(x in file for x in ['png', 'jpg', 'jpeg']) else Open_PNG(file, width/1.25)
    try:
        win.destroy()
    except:
        pass
    win = Toplevel()
    win.wm_title(title)
    win.geometry("%dx%d" % (basewidth, hsize))
    my_img = ImageTk.PhotoImage(img)
    my_label = Label(win, image=my_img)
    my_label.place(x=pop_up_x, y=pop_up_y)

def calibracionNube():
    global message, img, pop_up_x, pop_up_y, basewidth, hsize, win
    grafica = urlopen('http://siata.gov.co/CalidadAire/AnalisisDatos/Daniel/Daniel.txt')
    file = open('Daniel.txt', 'wb'); file.write(grafica.read()); file.close()
    df = read_csv('Daniel.txt', header=0, index_col=0)
    df.columns = df.columns.values.astype(int)
    try:
        string = 'Este es el estado actual de la nube %s ¿Desea continuar? \n\nFiltro PM2.5 NOVA = %s\nfiltro PM10 NOVA = ' \
                 '%s\nfiltro DF (50) = %s\nFecha Inicial = %s\nFecha Final = %s' \
                 % (int(df[df.index==nube.get()].index.values),df.loc[nube.get(),0], df.loc[nube.get(),1],
                    df.loc[nube.get(),2], df.loc[nube.get(),3].strip('\''), df.loc[nube.get(),4].strip('\''))
    except:
        string = 'No ha sido calibrada la nube'
    msg = messagebox.askquestion('Mensaje!', string,
                           icon='warning')
    if msg == 'no':
        filtro1.set(df.loc[nube.get(),0])
        filtro2.set(df.loc[nube.get(),1])
        check_df.set(1 if df.loc[nube.get(),2]=='Si' else 0)
        FechaiNube.set(df.loc[nube.get(),3].strip('\''))
        FechafNube.set(df.loc[nube.get(),4].strip('\''))
        return
    FechaiNube.set((datetime.now() - relativedelta(days=20)).strftime('%Y-%m-%d') if FechafNube.get() == ''
                   else FechaiNube.get())
    FechafNube.set((datetime.now()).strftime('%Y-%m-%d') if FechafNube.get() == '' else FechafNube.get())
    file = 'sudo su - ciudadanos_cientificos\n cd Ciudadanos_version2'
    command = 'python Daniel.py %d "%s" "%s" "%s" %s %s\n' % (nube.get(), FechaiNube.get(), FechafNube.get(),
                                                              'No' if check_df.get() != 1 else 'Si',
                                                              filtro1.get(), filtro2.get())
    endswith = 'ciudadanos_cientificos@gomita:~/Ciudadanos_version2$ '
    buff = comando_a_gomita(file, command, endswith, file_a_guardar='Daniel.txt')
    if not buff:
        return
    else:
        if "Calibracion_%d.pdf" % nube.get() in buff.split():
            try:
                message.destroy()
            except:pass
            message = Label(pes0, text='Calibró Nube %d' % nube.get(), anchor="e")
            message.place(x=places['mensaje_calibro'][0], y=places['mensaje_calibro'][1])

            descarga_un_archivo(
                'http://siata.gov.co/CalidadAire/CiudadanosCientificos/Graficas_Calibracion/Calibracion_%s.pdf' % nube.get(),
                'Descargas/', 'Calibracion.pdf', width=650, title="Calibracion Nube %s" % nube.get())
        else:
            try:
                message.destroy()
            except:pass
            message = Label(pes0, text='No Calibró Nube %d' % nube.get(), anchor="e")
            message.place(x=places['mensaje_calibro'][0], y=places['mensaje_calibro'][1])

def PDF_to_JPG(file, width):
    pages = convert_from_path(file, dpi=300)
    for page in pages:
        page.save(file.strip('.pdf')+'.JPG', 'JPEG')
    img = Image.open(file.strip('.pdf')+'.JPG')
    basewidth = width
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    return img, basewidth, hsize

botonCalibrarNube = Button(pes0, text='Calibrar \n Nube', command=calibracionNube, bg="#009",
                           fg="white").place(x=places['calibrar_nube'][0], y=places['calibrar_nube'][1])


#################################### Nube ####################################################
idx_nube = crear(pes0)
idx_nube.caja(nube, 8, places['caja_nube'][0], places['caja_nube'][1])

idx_estaciones = crear(pes0)

dict_vars = {"": sorted(['', 'MED-UNNV', 'MED-PJIC', 'MED-LAYE', 'ITA-CONC', 'GIR-SOSN', 'GIR-IECO', 'EST-METR', 'SAB-RAME',
                        'MED-VILL', 'MED-TESO', 'MED-SCRI', 'MED-BEME', 'MED-ARAN', 'MED-ALTA', 'EST-HOSP', 'ENV-HOSP',
                        'COP-CVID', 'CAL-JOAR', 'BEL-FEVE', 'BAR-TORR']),
             'PM2.5': sorted(['', 'SUR-TRAF', 'SAB-RAME', 'SAB-JOFE', 'MED-VILL', 'MED-UNNV', 'MED-TESO', 'MED-SELE',
                             'MED-SCRI', 'MED-PJIC', 'MED-LAYE', 'MED-BEME', 'MED-ARAN', 'MED-ALTA', 'ITA-CONC',
                             'ITA-CJUS', 'GIR-SOSN', 'EST-HOSP', 'ENV-HOSP', 'COP-CVID', 'CEN-TRAF', 'CAL-LASA',
                             'CAL-JOAR', 'BEL-FEVE', 'BAR-TORR', 'ICA', 'MED-MANT']),
             'PM2.5M': sorted(['', 'MED-PJIC', 'COP-IATO', 'BEL-SESB', 'ICA']),
             'PM10': sorted(['', 'SUR-TRAF', 'MED-UNFM', 'MED-PJIC', 'MED-MANT', 'MED-ITMR', 'MED-EXSA', 'ITA-POGO',
                            'ITA-CRSV', 'ITA-CONC', 'GIR-IECO', 'CEN-TRAF', 'CAL-PMER', 'CAL-JOAR', 'BEL-USBV', 'ICA']),
             'PM10M': sorted(['', 'SAB-CAMS', 'MED-PJIC', 'MED-MIRA', 'MED-CORA', 'ITA-PTAR', 'ITA-CRSV', 'EST-MAGO',
                             'COP-HSMA', 'CAL-PMER', 'BAR-HSVP']),
             'Ozono':sorted(['', 'MED-UNNV', 'MED-UDEM', 'MED-MIRA', 'MED-MANT', 'MED-LAYE', 'ITA-CONC', 'GIR-SOSN',
                             'CAL-LASA', 'BEL-USBV', 'BAR-PDLA']),
             'NOx':sorted(['', 'MED-UNNV', 'MED-UNFM', 'MED-PJIC', 'MED-MANT', 'MED-ITMR', 'ITA-CJUS', 'GIR-SOSN',
                           'EST-METR', 'BEL-USBV', 'CEN-TRAF', 'SUR-TRAF']),
             'NO2': sorted(['', 'MED-UNNV', 'MED-UNFM', 'MED-PJIC', 'MED-MANT', 'MED-ITMR', 'ITA-CJUS', 'GIR-SOSN',
                           'EST-METR', 'BEL-USBV', 'CEN-TRAF', 'SUR-TRAF']),
             'NO': sorted(['', 'MED-UNNV', 'MED-UNFM', 'MED-PJIC', 'MED-MANT', 'MED-ITMR', 'ITA-CJUS', 'GIR-SOSN',
                          'EST-METR', 'BEL-USBV']),
             'CO': sorted(['', 'SUR-TRAF', 'MED-PJIC', 'MED-MANT', 'GIR-SOSN', 'EST-METR', 'CEN-TRAF', 'ICA']),
             'SO2': sorted(['', 'MED-PJIC', 'GIR-SOSN', 'CEN-TRAF']),
             'TAire10_SSR': sorted(['', 'SUR-TRAF', 'MED-UNNV', 'MED-UDEM', 'MED-PJIC', 'MED-MANT', 'MED-LAYE',
                                   'ITA-CONC', 'ITA-CJUS', 'GIR-SOSN', 'GIR-IECO', 'EST-METR', 'CEN-TRAF',
                                   'CAL-LASA', 'BEL-USBV', 'BAR-PDLA']),
             'RGlobal_SSR':sorted(['',  'SUR-TRAF', 'MED-UNNV', 'MED-UDEM', 'MED-PJIC', 'MED-MANT', 'MED-LAYE',
                                   'ITA-CONC', 'ITA-CJUS', 'GIR-SOSN', 'GIR-IECO', 'EST-METR', 'CEN-TRAF',
                                   'CAL-LASA', 'BEL-USBV', 'BAR-PDLA']),
             'Meteorologia': sorted(['',   'SUR-TRAF', 'MED-UNNV', 'MED-UDEM', 'MED-PJIC', 'MED-MANT', 'MED-LAYE',
                                   'ITA-CONC', 'ITA-CJUS', 'GIR-SOSN', 'GIR-IECO', 'EST-METR', 'CEN-TRAF',
                                   'CAL-LASA', 'BEL-USBV', 'BAR-PDLA', 'SAB-SEMS', 'MED-ZOOL', 'MED-SIAT',
                                    'MED-PLMA', 'GIR-BOTJ', 'ITA-CODI']),
             'HAire10_SSR': sorted(['',  'SUR-TRAF', 'MED-UNNV', 'MED-UDEM', 'MED-PJIC', 'MED-LAYE', 'ITA-CONC',
                                   'ITA-CJUS', 'GIR-SOSN', 'GIR-IECO', 'EST-METR', 'CAL-LASA', 'BEL-USBV',
                                   'BAR-PDLA']),
             'PLiquida_SSR': sorted(['',  'SUR-TRAF', 'MED-UNNV', 'MED-UDEM', 'MED-PJIC', 'MED-LAYE', 'ITA-CONC',
                                   'ITA-CJUS', 'GIR-SOSN', 'GIR-IECO', 'EST-METR', 'CAL-LASA', 'BEL-USBV',
                                   'BAR-PDLA', 'SAB-SEMS', 'MED-SIAT', 'MED-PLMA', 'ITA-CODI', 'GIR-BOTJ',
                                   'CEN-TRAF']),
             'Omega': ['', '3h', '6h', '12h', '24h', '48h'],
             'Consolidados_Anuales':sorted(['', 'CEN-TRAF', 'GIR-SOSN', 'MED-PJIC', 'MED-UNFM', 'SUR-TRAF',
                                            'BEL-USBV', 'ITA-CJUS', 'MED-ITMR', 'MED-UNNV', 'BAR-PDLA',
                                            'CAL-LASA', 'ITA-CONC', 'MED-LAYE', 'MED-MIRA', 'MED-UDEM',
                                            'CAL-JOAR', 'GIR-IECO', 'ITA-POGO', 'ITA-CRSV', 'BEL-FEVE',
                                            'BAR-TORR', 'COP-CVID', 'EST-HOSP', 'ENV-HOSP', 'MED-VILL',
                                            'SAB-JOFE', 'SAB-RAME', 'MED-SELE', 'MED-SCRI', 'MED-ALTA',
                                            'MED-ARAN', 'MED-BEME']),
             'Ruido': sorted(['', 'SAB-SEMS', 'MED-ZOOL', 'MED-SIAT', 'MED-PLMA', 'MED-PJIC', 'ITA-CODI',
                             'GIR-SOSN', 'GIR-BOTJ', 'CEN-TRAF']),
             'PM2.5 Minutales': ['3h', '24h'],
             'Rosas Bivariadas':['', 'PM25', 'PM10', 'NOx', 'NO', 'NO2', 'CO', 'OZONO']
             }
#####################################################################################################################
def grafico_serie(Tipo):
    send_copy(send.get())
    comando_a_gomita('cd /home/calidadaire/JupyterNotebooks/dparraho/', 'python Generar%s.py "%s" "%s" "%s"' %
                     (Tipo, variable2.get(), 'Temporal/%s'%send.get(), Textsavegraph.get()),
                     'dparraho@gomita:/home/calidadaire/JupyterNotebooks/dparraho$ ',
                     file_a_guardar='Temporal/%s_*.pdf'%Textsavegraph.get(), specific_file='graphs_from_app/')
variable2['values'] = ('PM2.5', 'PM2.5M', 'PM10', 'PM10M', 'Ozono', 'NOx', 'NO2', 'NO', 'CO', 'SO2', 'TAire10_SSR',
                      'RGlobal_SSR', 'HAire10_SSR', 'PLiquida_SSR')


def validacion_meteo(rand):
    comando_a_gomita('cd /home/calidadaire/JupyterNotebooks/dparraho/', 'python %scalidad.py "%s" "%s"' %
                     (rand, FechaiMeteo.get(), FechafMeteo.get()),
                     'dparraho@gomita:/home/calidadaire/JupyterNotebooks/dparraho$ ')
def validacion_meteo_estacion():
    comando_a_gomita('cd /home/calidadaire/JupyterNotebooks/dparraho/', 'python calidad.py "%s" "%s" "%s" "%s"' %
                     (FechaiMeteo.get(), FechafMeteo.get(), EstMeteoInterna.get(), MeteoInternaVariable.get()),
                     'dparraho@gomita:/home/calidadaire/JupyterNotebooks/dparraho$ ')




variable['values'] = ("", 'PM2.5', 'PM2.5M', 'PM10', 'PM10M', 'Ozono', 'NOx', 'NO2', 'NO', 'CO', 'SO2', 'TAire10_SSR',
                      'RGlobal_SSR', 'Meteorologia', 'HAire10_SSR', 'PLiquida_SSR', 'Omega', 'Consolidados_Anuales',
                      'Ruido', 'PM2.5 Minutales', 'Rosas Bivariadas')

EstMeteoInterna['values'] = ['GIR-SOSN', 'MED-PJIC', 'CEN-TRAF', 'MED-UNNV', 'ITA-CJUS','CAL-LASA', 'BEL-USBV',
                             'ITA-CONC', 'BAR-PDLA', 'MED-UDEM','MED-MIRA', 'MED-LAYE', 'SUR-TRAF', 'MED-ITMR']
EstMeteoInterna.place(x=places2['estaciones_internas'][0], y=places2['estaciones_internas'][1])
EstMeteoInterna.current(0)
MeteoInternaVariable['values'] = ('temperatura_interna', 'humedad_interna')
MeteoInternaVariable.place(x=places2['temperatura_o_humedad'][0], y=places2['temperatura_o_humedad'][1])
MeteoInternaVariable.current(0)

idx_validar = crear(pes1)
idx_validar.label('El boton a continuación invalida datos'+
                  '\nde meteorologia interna del shelter de'+
                  '\nacuerdo con los rangos del manual, 15 '+
                  'y 15.5. \nSe demora considerablemente '+
                  'si se valida un mes entero', places2['texto_internas'][0], places2['texto_internas'][1], bg=None)
botonInValidar = Button(pes1, text='Invalidar\nMeteo', command=lambda :validacion_meteo(''), bg="red",
                        fg="white").place(x=places2['invalidar_internas'][0], y=places2['invalidar_internas'][1])
botonValidar = Button(pes1, text='Validar\nMeteo', command=lambda : validacion_meteo('r_'), bg="gray",
                      fg="white").place(x=places2['validar_internas'][0], y=places2['validar_internas'][1])
botonValidarEst = Button(pes1, text='Validar\nMeteo Unica', command=validacion_meteo_estacion, bg="Red",
                         fg="white").place(x=places2['validar_una_interna'][0], y=places2['validar_una_interna'][1])
variable2.place(x=places2['color_variable'][0], y=places2['color_variable'][1])
variable2.current(0)
idx_variable2 = crear(pes1)
idx_variable2.label('Color', places2['label_color_variable'][0], places2['label_color_variable'][1], bg=None)
idx_send = crear(pes1)
idx_send.label('Archivo',  places2['label_archivo_enviar'][0], places2['label_archivo_enviar'][1], bg=None)
idx_send.caja(send, 20, places2['box_archivo_enviar'][0], places2['box_archivo_enviar'][1])
botonSerie = Button(pes1, text='Serie', command=lambda: grafico_serie('Serie'), bg="#009",
                           fg="white").place(x=places2['hacer_serie'][0], y=places2['hacer_serie'][1])
botonHist = Button(pes1, text='Histograma', command=lambda: grafico_serie('Histograma'), bg="#009",
                           fg="white").place(x=places2['hacer_histograma'][0], y=places2['hacer_histograma'][1])
botonHist = Button(pes1, text='Histograma ICA', command=lambda: grafico_serie('HistogramaICA'), bg="#009",
                           fg="white").place(x=places2['hacer_histograma_ICA'][0], y=places2['hacer_histograma_ICA'][1])

idx_textsave = crear(pes1)
idx_textsave.label('TextSave', places2['label_textsave_figuras'][0], places2['label_textsave_figuras'][1], bg=None)
idx_textsave.caja(Textsavegraph, 20, places2['box_textsave_figuras'][0], places2['box_textsave_figuras'][1])
################################################################################################################333

variable.place(x=places['variable_para_consultar'][0], y=places['variable_para_consultar'][1])
variable.current(1)
variable.bind("<<ComboboxSelected>>", selection)

estacion['values'] = dict_vars[variable.get()]
estacion.place(x=places['estacion_para_consultar'][0], y=places['estacion_para_consultar'][1])
estacion.current(len(estacion['values'])-1)



idx_descarga = crear(pes0)
idx_descarga.caja(descarga, 20, places['textsave_consulta'][0], places['textsave_consulta'][1])

botonEstacion = Button(pes0, text="Consultar\nVariable", command=consultarEstacion, bg="#009",
                       fg="white").place(x=places['consultar_variable'][0], y=places['consultar_variable'][1])

botonNube = Button(pes0, text="Estado",
                   command=lambda : descarga_un_archivo('http://siata.gov.co/CalidadAire/AnalisisDatos/Natalia/Ciudadanos/Graficas_Estado/Estado_%s.pdf'%nube.get(),
                                                        'Descargas/', 'Estado.pdf', width=700,
                                                        title='Estado de la Nube %s' % nube.get()),
                   bg="#009", fg="white").place(x=places['boton_estado'][0],y=places['boton_estado'][1])
botonCal = Button(pes0, text="Calibracion",
                   command=lambda : descarga_un_archivo('http://siata.gov.co/CalidadAire/CiudadanosCientificos/Graficas_Calibracion/Calibracion_%s.pdf'%nube.get(),
                                                        'Descargas/', 'Calibracion.pdf', width=700,
                                                        title='Calibracion de la Nube %s' % nube.get()),
                   bg="#009", fg="white").place(x=places['boton_calibracion'][0],y=places['boton_calibracion'][1])

botonEspectrometro = Button(pes0, text="%s \nEspectrómetro"%('Actualizar' if glob('Espectrometro/*pdf') else 'Descargar'),
                       command=espectrometro, bg="indianred", fg="black").place(x=places['espectrometro'][0],y=places['espectrometro'][1])
botonDatosNube = Button(pes0, text='Descargar\nDatos Nube', command=datosNube, bg="#009",
                        fg="white").place(x=places['descargar_nubes'][0],y=places['descargar_nubes'][1])
#phot = PhotoImage('ConteoICA_SUR-TRAF.gif')
#panel = Label(pes0, text='Alo', image=phot)
#panel.place(x=300, y=300)

idx2_fechai = crear(pes0)
idx2_fechai.caja(FechaiMeteo, 15,places['box_fechai_meteo'][0], places['box_fechai_meteo'][1])
idx2_fechai.label('Fecha inicial',places['label_fechai_meteo'][0], places['label_fechai_meteo'][1])
idx2_fechaf = crear(pes0)
idx2_fechaf.caja(FechafMeteo, 15, places['box_fechaf_meteo'][0], places['box_fechaf_meteo'][1])
idx2_fechaf.label('Fecha final', places['label_fechaf_meteo'][0], places['label_fechaf_meteo'][1])
idx2_fechai = crear(pes1)
idx2_fechai.caja(FechaiMeteo, 15,places2['box_fechai_meteo'][0], places2['box_fechai_meteo'][1])
idx2_fechai.label('Fecha inicial',places2['label_fechai_meteo'][0], places2['label_fechai_meteo'][1], bg=None)
idx2_fechaf = crear(pes1)
idx2_fechaf.caja(FechafMeteo, 15,places2['box_fechaf_meteo'][0], places2['box_fechaf_meteo'][1])
idx2_fechaf.label('Fecha final', places2['label_fechaf_meteo'][0], places2['label_fechaf_meteo'][1], bg=None)


def GraficaMeteo(local_var):
    global basewidth, hsize, pop_up_x, pop_up_y, img, win, progress
    # ListaAchivos = glob('%s_interna_*.pdf'%local_var)
    _, ListaArchivos = sshconsulta('/var/www/CalidadAire/AnalisisDatos/Daniel/', folder='', local_var=local_var)
    links = []
    for i in ListaArchivos:
        links.append('http://siata.gov.co/CalidadAire/AnalisisDatos/Daniel/%s' % i)
        graficaestado = urlopen(
            'http://siata.gov.co/CalidadAire/AnalisisDatos/Daniel/%s' % i)
        file = open(i, 'wb'); file.write(graficaestado.read()); file.close()

    screen_h = int(1366)
    screen_v = 768 * 0.9
    divisor_h = 5
    pos = [(0, i) for i in range(0, screen_h-1, int(screen_h/divisor_h))] \
          + [(int(screen_v/3), i) for i in range(0, screen_h-1, int(screen_h/divisor_h))] \
          + [(int(screen_v/3)*2, i) for i in range(0, screen_h-1, int(screen_h/divisor_h))]

    multiple_popup('Gráficas %s' % local_var, screen_h, screen_v, divisor_h, ListaArchivos, pos, links)

def actualizar_meteo():
     comando_a_gomita('cd /home/calidadaire/JupyterNotebooks/dparraho/', 'python GenerarHumedad.py "%s" "%s"' %
                      (FechaiMeteo.get(), FechafMeteo.get()), 'dparraho@gomita:/home/calidadaire/JupyterNotebooks/dparraho$ ',
                      file_a_guardar='Figuras/Anexos/humedad_interna_*.pdf Figuras/Anexos/temperatura_interna_*.pdf',
                      specific_file='figuras_meteo/')

bytes=0

maxbytes = 960
def read_bytes():
    '''simulate reading 500 bytes; update progress bar'''
    global bytes, progress, maxbytes
    bytes += 500
    #progress["value"] = bytes
    if bytes < maxbytes:
        # read more bytes after 100 ms
        Tk.after(pes0, 100, read_bytes)


########################################## Descarga Datos #########################################################
def descargar_data():
    comando_a_gomita('cd /home/calidadaire/JupyterNotebooks/dparraho/', 'python GenerarDatos.py "%s" "%s" "%s" "%s"' %
                     (varsDescargar.get(), fileDescarga.get(), FechaiDatos.get(), FechafDatos.get()),
                     'dparraho@gomita:/home/calidadaire/JupyterNotebooks/dparraho$ ',
                     file_a_guardar='Peticiones/%s'%fileDescarga.get(),
                     specific_file='datos_red/')

botonConteo = Button(pes0, text="Descargar\nDatos", command=descargar_data, bg="#009",
                       fg="white").place(x=places['descargar_red'][0], y=places['descargar_red'][1])
idx_fechai = crear(pes0)
idx_fechai.caja(FechaiDatos, 10, places['box_fechai_red'][0], places['box_fechai_red'][1])
idx_fechai.label('Fecha inicial', places['label_fechai_red'][0], places['label_fechai_red'][1])
FechaiDatos.set((datetime.now() - relativedelta(days=20)).strftime('%Y-%m-01 01:00'))

idx_fechai = crear(pes0)
idx_fechai.caja(FechafDatos, 10, places['box_fechaf_red'][0], places['box_fechaf_red'][1])
idx_fechai.label('Fecha final', places['label_fechaf_red'][0], places['label_fechaf_red'][1])
FechafDatos.set((datetime.now()).strftime('%Y-%m-%d 00:00'))

varsDescargar['values'] = ('PM2.5', 'PM2.5M', 'PM10', 'PM10M', 'Ozono', 'NOx', 'NO2', 'NO', 'CO', 'SO2', 'BC')
varsDescargar.place(x=places['variables_red'][0], y=places['variables_red'][1])
varsDescargar.current(0)

idx_fechai = crear(pes0)
idx_fechai.caja(fileDescarga, 20,places['textsave_red'][0], places['textsave_red'][1])
###################################################################################################################
idx_shelter = crear(pes0)
idx_shelter.label('Temperatura y Humedad interna shelter', places['label_internas'][0], places['label_internas'][1])
botonGraficos = Button(pes0, text='Actualizar\nGráficos', command=actualizar_meteo, bg="#009",
                       fg="white").place(x=places['actualizar_internas'][0], y=places['actualizar_internas'][1])
botonShowT = Button(pes0, text='Mostrar\nTemperatura', command=lambda: GraficaMeteo('temperatura'), bg="salmon",
                    fg="black").place(x=places['mostrar_temperatura'][0], y=places['mostrar_temperatura'][1])
botonShowH = Button(pes0, text='Mostrar\nHumedad', command=lambda: GraficaMeteo('humedad'), bg="salmon",
                    fg="black").place(x=places['mostrar_humedad'][0], y=places['mostrar_humedad'][1])

ventana.mainloop()
