'''
Práctica realizada por:
    - Alejandr Garcia Lavandera
    - Angel Antolin Caramazana
Grupo: T3. Subgrupo de laboratorio: Z7
'''

import wx
import time
from externo import Mazo, Estrategia, CartaBase

# Clase que representa las Cartas
class Carta(CartaBase):
    # Devuelve el palo en un rango de 0-51
    
    # Funcion que traduce el indice de la carta en el palo
    @property
    def palo(self):
        if self.ind >= 0 and self.ind <= 12:
            return "♠"  # [PICAS]
        elif self.ind >= 13 and self.ind <= 25:
            return "♣" # [TREBOLES]
        elif self.ind >= 26 and self.ind <= 38:
            return "♦" # [DIAMANTES]
        else:
            return "♥" # [CORAZONES]

    # Funcion que traduce el indice de la carta en un valor facial
    @property
    def numCarta(self):

        if self.ind % 13 + 1 == 1:
            return "A"
        elif self.ind % 13 + 1 == 11:
            return "J"
        elif self.ind % 13 + 1 == 12:
            return "Q"
        elif self.ind % 13 + 1 == 13:
            return "K"
        else:
            return self.ind % 13 + 1
        
        

# Clase para representar cada mano (Croupier y jugador)
class Mano():
    def __init__(self):
        
        # Variables referidas a las propiedades de cada mano
        self.cartas = []            # Array que almacena las cartas de la mano
        self.nomMano = "Mano"       # Variable para el nombre de la mano
        self.valorMano = 0          # Variable representa el valor total de la mano
        self.estadoMano = "Activa"  # Variable que representa el estado de la mano
        self.apuestaMano = 0        # Variablee que almacena el valor de la apuesta para la mano
        
        # Variables para localizar la mano
        self.sizerMano = ''         # Posicion de la mano dentro de la ventana
        self.panelMano = ''         # ""
        self.sizerCartasMano = ''   # ""
        self.cartasIMGs = []        # Almacen de las cartas visualizadas en la ventana
        self.detallesMano = ''      # Datos de la mano (izq)
        self.seleccionMano = ''     # Boton para seleccionar la mano a la hoar de realizar una accion
        
    # Calcula y establece el valor de la mano pasada como atributo
    def valorMano(self, mano):
        mano.valorMano = 0
        
        for carta in mano.cartas:
            mano.valorMano += carta.valor
            
        for carta in mano.catas:
            if carta.valor == 1 and mano.valorMano <= 11:
                mano.valorMano += 10
    
    def estadoMano(self, mano):
        if mano.valorMano <= 21:
            mano.estadoMano = "Activa"
        elif mano.valorMano > 21:
            mano.estadoMano = "Pasada"
        

# Clase para almacenar todas las variables necesarias para el programa
class Variables():
    # Variables "globales" para el codigo
    def estableceVariables(self):
        # Creamos e inicializamos todas las variables necesarias
        
        # Variables para los jugadores
        self.jugador = [Mano()]     # El jugador tiene > 1 Manos
        self.croupier = Mano()      # El croupier tiene = 1 Mano
        
        # Variables para el control de la partida
        self.finPartida = False
        self.finTurnoJugador = False
        self.finTurnoCroupier = False
        
        # Variable para el modo de ejecucion del programa 
        self.modoEjecucion = ""
        
        # Variable para la seleccion de la mano a la hora de realizar la accion
        self.seleccionMano = 0



class DIALOGOAPUESTA(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: DIALOGOAPUESTA.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((245, 229))
        self.SetTitle("BlackJack - Apuesta")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./icono.jpeg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Elija Apuesta:"), wx.VERTICAL)
        sizer_1.Add(sizer_3, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 25)

        self.radio_btn_1 = wx.RadioButton(self, wx.ID_ANY, u"2€")
        sizer_3.Add(self.radio_btn_1, 0, wx.BOTTOM, 0)

        self.radio_btn_2 = wx.RadioButton(self, wx.ID_ANY, u"10€")
        sizer_3.Add(self.radio_btn_2, 0, wx.BOTTOM, 0)

        self.radio_btn_3 = wx.RadioButton(self, wx.ID_ANY, u"50€")
        sizer_3.Add(self.radio_btn_3, 0, wx.BOTTOM, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        sizer_2.AddButton(self.button_OK)

        sizer_2.Realize()

        self.SetSizer(sizer_1)

        self.SetAffirmativeId(self.button_OK.GetId())

        self.Layout()

        self.Bind(wx.EVT_RADIOBUTTON, self.apuesta2, self.radio_btn_1)
        self.Bind(wx.EVT_RADIOBUTTON, self.apuesta10, self.radio_btn_2)
        self.Bind(wx.EVT_RADIOBUTTON, self.apuesta50, self.radio_btn_3)
        self.Bind(wx.EVT_BUTTON, self.apostarPartida, self.button_OK)
        # end wxGlade
        
        # Creo una variable par almacenar la apuesta seleccionado
        self.valorApuesta = 0

    # Actualizo el valor de la apuesta segun la opcion elegida
    def apuesta2(self, event):  # wxGlade: DIALOGOAPUESTA.<event_handler>
        self.valorApuesta = 2
        return self.valorApuesta

    def apuesta10(self, event):  # wxGlade: DIALOGOAPUESTA.<event_handler>
        self.valorApuesta = 10
        return self.valorApuesta

    def apuesta50(self, event):  # wxGlade: DIALOGOAPUESTA.<event_handler>
        self.valorApuesta = 2
        return self.valorApuesta

    def apostarPartida(self, event):  # wxGlade: DIALOGOAPUESTA.<event_handler>
        # Creo la ventana para iniciar el juego manual
        self.vManual = manual(None, wx.ID_ANY, "")
        # Oculto la ventana actual
        self.Hide()
        #Muestro la ventana del modo de juego manual
        # self.vManual.Show()
        event.Skip()

# end of class DIALOGOAPUESTA

class manual(wx.Frame):
    
    # Creo un acceso a las variables globales
    varGlobales = Variables()
    varGlobales.estableceVariables()
    
    # Creo el mazo para la partida
    estrategia = Estrategia(2)
    mazo = Mazo(Carta, estrategia)
    
    # Variables - infor partidas
    numPartidas = 1     # Iniciamos el contador de partidas con 1
    balancePartida = 0  # Iniciamos el balance de la partida en 0
    balanceGlobal = 0   # Iniciamos el balance en 0
    
    
    
    def __init__(self, *args, **kwds):
        # begin wxGlade: manual.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("BlackJack - Manual")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./icono.jpeg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        self.bitmap_button_1 = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("./luigi_dealer.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_1.SetMinSize((200, 200))
        sizer_2.Add(self.bitmap_button_1, 0, wx.TOP, 10)

        sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Modo de Juego:"), wx.HORIZONTAL)
        sizer_2.Add(sizer_3, 0, wx.TOP, 20)

        self.radio_btn_1 = wx.RadioButton(self.panel_1, wx.ID_ANY, "Manual")
        sizer_3.Add(self.radio_btn_1, 0, 0, 0)

        self.radio_btn_2 = wx.RadioButton(self.panel_1, wx.ID_ANY, "Automatico")
        sizer_3.Add(self.radio_btn_2, 0, 0, 0)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_4, 0, wx.EXPAND | wx.TOP, 20)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, "Retardo:")
        sizer_4.Add(label_1, 0, 0, 0)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "25", style=wx.TE_RIGHT)
        sizer_4.Add(self.text_ctrl_1, 0, 0, 0)

        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, "ms.")
        sizer_4.Add(label_2, 0, 0, 0)

        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Accion:"), wx.VERTICAL)
        sizer_2.Add(sizer_5, 0, wx.EXPAND | wx.TOP, 20)

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, "PEDIR")
        sizer_5.Add(self.button_1, 0, wx.EXPAND, 0)

        self.button_2 = wx.Button(self.panel_1, wx.ID_ANY, "DOBLAR")
        sizer_5.Add(self.button_2, 0, wx.EXPAND, 0)

        self.button_3 = wx.Button(self.panel_1, wx.ID_ANY, "CERRAR")
        sizer_5.Add(self.button_3, 0, wx.EXPAND, 0)

        self.button_4 = wx.Button(self.panel_1, wx.ID_ANY, "SEPARAR")
        sizer_5.Add(self.button_4, 0, wx.EXPAND, 0)

        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Numero Partidas:"), wx.VERTICAL)
        sizer_2.Add(sizer_6, 0, wx.EXPAND | wx.TOP, 165)

        label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, "0")
        label_3.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        sizer_6.Add(label_3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)

        sizer_7 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Balance Global"), wx.VERTICAL)
        sizer_2.Add(sizer_7, 0, wx.EXPAND | wx.TOP, 10)

        label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, "0")
        label_4.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        sizer_7.Add(label_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)

        sizer_8 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Balance Partida Actual:"), wx.VERTICAL)
        sizer_2.Add(sizer_8, 0, wx.EXPAND | wx.TOP, 10)

        label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, "0")
        label_5.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        sizer_8.Add(label_5, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)

        sizer_9 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, u"Cuenta Atrás:"), wx.VERTICAL)
        sizer_2.Add(sizer_9, 0, wx.EXPAND | wx.TOP, 10)

        label_6 = wx.StaticText(self.panel_1, wx.ID_ANY, "10")
        label_6.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        sizer_9.Add(label_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)

        self.panel_juego = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.panel_juego, 1, wx.EXPAND, 0)

        sizer_10 = wx.BoxSizer(wx.VERTICAL)

        self.panel_croupier = wx.Panel(self.panel_juego, wx.ID_ANY)
        sizer_10.Add(self.panel_croupier, 1, wx.EXPAND, 0)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)

        label_7 = wx.StaticText(self.panel_croupier, wx.ID_ANY, "Croupier\n(0)\nActiva")
        label_7.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_11.Add(label_7, 0, 0, 0)

        sizer_11.Add((0, 0), 0, 0, 0)

        self.panel_2_control = wx.Panel(self.panel_croupier, wx.ID_ANY)
        sizer_11.Add(self.panel_2_control, 1, wx.EXPAND, 0)

        self.panel_jugador = wx.Panel(self.panel_juego, wx.ID_ANY)
        sizer_10.Add(self.panel_jugador, 1, wx.EXPAND, 0)

        sizer_jugador = wx.BoxSizer(wx.VERTICAL)

        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_jugador.Add(sizer_12, 1, wx.EXPAND, 0)

        label_8 = wx.StaticText(self.panel_jugador, wx.ID_ANY, "(Valor)\nApuesta\nEstado")
        label_8.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_12.Add(label_8, 0, 0, 0)

        sizer_12.Add((0, 0), 0, 0, 0)

        self.panel_jugador_control = wx.Panel(self.panel_jugador, wx.ID_ANY)
        sizer_12.Add(self.panel_jugador_control, 1, wx.EXPAND, 0)

        self.panel_jugador.SetSizer(sizer_jugador)

        self.panel_croupier.SetSizer(sizer_11)

        self.panel_juego.SetSizer(sizer_10)

        self.panel_1.SetSizer(sizer_1)

        sizer_1.Fit(self)
        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.curiosidad, self.bitmap_button_1)
        self.Bind(wx.EVT_RADIOBUTTON, self.modoManual, self.radio_btn_1)
        self.Bind(wx.EVT_RADIOBUTTON, self.modoAutomatico, self.radio_btn_2)
        self.Bind(wx.EVT_BUTTON, self.accionPedir, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.accionDoblar, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.accionCerrar, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.accionSeparar, self.button_4)
        # end wxGlade

    def curiosidad(self, event):  # wxGlade: manual.<event_handler>
        print("Event handler 'curiosidad' not implemented!")
        event.Skip()

    def modoManual(self, event):  # wxGlade: manual.<event_handler>
        print("Event handler 'modoManual' not implemented!")
        event.Skip()

    def modoAutomatico(self, event):  # wxGlade: manual.<event_handler>
        print("Event handler 'modoAutomatico' not implemented!")
        event.Skip()

    def accionPedir(self, event):  # wxGlade: manual.<event_handler>
        print("Event handler 'accionPedir' not implemented!")
        event.Skip()

    def accionDoblar(self, event):  # wxGlade: manual.<event_handler>
        print("Event handler 'accionDoblar' not implemented!")
        event.Skip()

    def accionCerrar(self, event):  # wxGlade: manual.<event_handler>
        print("Event handler 'accionCerrar' not implemented!")
        event.Skip()

    def accionSeparar(self, event):  # wxGlade: manual.<event_handler>
        print("Event handler 'accionSeparar' not implemented!")
        event.Skip()

# end of class manual

class BlackJack(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: BlackJack.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((400, 250))
        self.SetTitle("BlackJack")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./icono.jpeg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.bitmap_button_1 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./blackjack.jpg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        sizer_1.Add(self.bitmap_button_1, 0, wx.EXPAND, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        sizer_2.AddButton(self.button_OK)

        sizer_2.Realize()

        self.SetSizer(sizer_1)

        self.SetAffirmativeId(self.button_OK.GetId())

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.blackjackSonido, self.bitmap_button_1)
        self.Bind(wx.EVT_BUTTON, self.okBlackJack, self.button_OK)
        # end wxGlade

    def blackjackSonido(self, event):  # wxGlade: BlackJack.<event_handler>
        print("Event handler 'blackjackSonido' not implemented!")
        event.Skip()

    def okBlackJack(self, event):  # wxGlade: BlackJack.<event_handler>
        print("Event handler 'okBlackJack' not implemented!")
        event.Skip()

# end of class BlackJack

class volverJugar(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: volverJugar.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle("BlackJack - Volver a Jugar")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.bitmap_button_1 = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("./volverJugar.jpeg", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        sizer_1.Add(self.bitmap_button_1, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.button_YES = wx.Button(self, wx.ID_YES, "")
        self.button_YES.SetDefault()
        sizer_2.AddButton(self.button_YES)

        self.button_NO = wx.Button(self, wx.ID_NO, "")
        sizer_2.AddButton(self.button_NO)

        sizer_2.Realize()

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.SetAffirmativeId(self.button_YES.GetId())

        self.Layout()
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.sonidoPregunta, self.bitmap_button_1)
        self.Bind(wx.EVT_BUTTON, self.inicioPartidaNueva, self.button_YES)
        self.Bind(wx.EVT_BUTTON, self.finPartida, self.button_NO)
        # end wxGlade

    def sonidoPregunta(self, event):  # wxGlade: volverJugar.<event_handler>
        print("Event handler 'sonidoPregunta' not implemented!")
        event.Skip()

    def inicioPartidaNueva(self, event):  # wxGlade: volverJugar.<event_handler>
        print("Event handler 'inicioPartidaNueva' not implemented!")
        event.Skip()

    def finPartida(self, event):  # wxGlade: volverJugar.<event_handler>
        print("Event handler 'finPartida' not implemented!")
        event.Skip()

# end of class volverJugar

class inicio(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: inicio.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("BlackJack - Inicio")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./icono.jpeg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.panel_1.SetBackgroundColour(wx.Colour(0, 0, 0))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.bitmap_button_1 = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("./fondo.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        sizer_1.Add(self.bitmap_button_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.panel_1.SetSizer(sizer_1)

        sizer_1.Fit(self)
        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.seleccionModo, self.bitmap_button_1)
        # end wxGlade

    def seleccionModo(self, event):  # wxGlade: inicio.<event_handler>
        # Creo la ventana para seleccionar el modo de ejecucion del programa
        vSelecModo = ventanaModo(None, wx.ID_ANY, "")
        # Muestro la ventana creada
        vSelecModo.Show()
        # Cierro la ventana actual
        self.Hide()
        
        event.Skip()

# end of class inicio

class ventanaModo(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ventanaModo.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((300, 186))
        self.SetTitle("BlackJack - Seleccion del Modo")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Selecciona un modo de juego:"), wx.VERTICAL)
        sizer_1.Add(sizer_3, 1, wx.ALL | wx.EXPAND, 20)

        self.radio_btn_1 = wx.RadioButton(self, wx.ID_ANY, "Manual")
        sizer_3.Add(self.radio_btn_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.radio_btn_2 = wx.RadioButton(self, wx.ID_ANY, u"Automático")
        sizer_3.Add(self.radio_btn_2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        sizer_2.AddButton(self.button_OK)

        sizer_2.Realize()

        self.SetSizer(sizer_1)

        self.SetAffirmativeId(self.button_OK.GetId())

        self.Layout()

        self.Bind(wx.EVT_RADIOBUTTON, self.modoManual, self.radio_btn_1)
        self.Bind(wx.EVT_RADIOBUTTON, self.modoAutomatico, self.radio_btn_2)
        self.Bind(wx.EVT_BUTTON, self.inicioPartida, self.button_OK)
        # end wxGlade
        
        # Creo una variable para controlar la seleccion del modo de juego:
            # Por defecto sera el modo manual
        self.modoSleccionado = False
        
    def modoManual(self, event):  # wxGlade: ventanaModo.<event_handler>
        # Establezco la variable en modo manual
        self.modoSleccionado = False
        return self.modoSleccionado

    def modoAutomatico(self, event):  # wxGlade: ventanaModo.<event_handler>
        # Establzco la variable en modo automatico
        self.modoSleccionado = True
        return self.modoSleccionado

    def inicioPartida(self, event):  # wxGlade: ventanaModo.<event_handler>
        # Compruebo el valor de la variable del control del modo de juego, en funcion de su valor, abro una ventana
        if self.modoSleccionado == False: # Modo manual
            # Creo la ventana para la apuesta y para el modo manual
            vSelecApuesta = DIALOGOAPUESTA(None, wx.ID_ANY, "")
            vManual = manual(None, wx.ID_ANY, "")
            # Creo la variable para la ventan de inicio y la oculto
            vInicio = inicio(None, wx.ID_ANY, "")
            vInicio.Hide()
            # Muestro la ventana de la apuesta
            vManual.Show()
            vSelecApuesta.Show()
        
        else: # Modo automatico
            # Creo la ventana para insertar el nº de partidas y el modo automatico
            vNumPartidas = numeroPartidas(None, wx.ID_ANY, "")
            vAutomatico = automatico(None, wx.ID_ANY, "")
            # Creo la variable para la ventan de inicio y la oculto
            vInicio = inicio(None, wx.ID_ANY, "")
            vInicio.Hide()
            # Muestro la ventana de la apuesta
            vAutomatico.Show()
            vNumPartidas.Show()
        event.Skip()

# end of class ventanaModo

class numeroPartidas(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: numeroPartidas.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((400, 170))
        self.SetTitle("BlackJack - Numero Partidas")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./icono.jpeg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Inserte el numero de partidas que desea jugar:"), wx.HORIZONTAL)
        sizer_1.Add(sizer_3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 23)

        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "Inserte aqui...", style=wx.TE_LEFT)
        sizer_3.Add(self.text_ctrl_1, 0, wx.ALL, 5)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        sizer_2.AddButton(self.button_OK)

        sizer_2.Realize()

        self.SetSizer(sizer_1)

        self.SetAffirmativeId(self.button_OK.GetId())

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.inicioAutomatico, self.button_OK)
        # end wxGlade

    def inicioAutomatico(self, event):  # wxGlade: numeroPartidas.<event_handler>
        print("Event handler 'inicioAutomatico' not implemented!")
        event.Skip()

# end of class numeroPartidas

class automatico(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: automatico.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("BlackJack - Automatico")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./icono.jpeg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        self.bitmap_button_1 = wx.BitmapButton(self.panel_1, wx.ID_ANY, wx.Bitmap("./luigi_dealer.png", wx.BITMAP_TYPE_ANY))
        self.bitmap_button_1.SetMinSize((200, 200))
        sizer_2.Add(self.bitmap_button_1, 0, wx.TOP, 10)

        sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Modo de Juego:"), wx.HORIZONTAL)
        sizer_2.Add(sizer_3, 0, wx.TOP, 20)

        self.radio_btn_1 = wx.RadioButton(self.panel_1, wx.ID_ANY, "Manual")
        sizer_3.Add(self.radio_btn_1, 0, 0, 0)

        self.radio_btn_2 = wx.RadioButton(self.panel_1, wx.ID_ANY, "Automatico")
        sizer_3.Add(self.radio_btn_2, 0, 0, 0)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_4, 0, wx.EXPAND | wx.TOP, 20)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, "Retardo:")
        sizer_4.Add(label_1, 0, 0, 0)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "25", style=wx.TE_RIGHT)
        sizer_4.Add(self.text_ctrl_1, 0, 0, 0)

        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, "ms.")
        sizer_4.Add(label_2, 0, 0, 0)

        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Accion:"), wx.VERTICAL)
        sizer_2.Add(sizer_5, 0, wx.EXPAND | wx.TOP, 20)

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, "PEDIR")
        sizer_5.Add(self.button_1, 0, wx.EXPAND, 0)

        self.button_2 = wx.Button(self.panel_1, wx.ID_ANY, "DOBLAR")
        sizer_5.Add(self.button_2, 0, wx.EXPAND, 0)

        self.button_3 = wx.Button(self.panel_1, wx.ID_ANY, "CERRAR")
        sizer_5.Add(self.button_3, 0, wx.EXPAND, 0)

        self.button_4 = wx.Button(self.panel_1, wx.ID_ANY, "SEPARAR")
        sizer_5.Add(self.button_4, 0, wx.EXPAND, 0)

        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Numero Partidas:"), wx.VERTICAL)
        sizer_2.Add(sizer_6, 0, wx.EXPAND | wx.TOP, 165)

        label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, "0")
        label_3.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        sizer_6.Add(label_3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)

        sizer_7 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Balance Global"), wx.VERTICAL)
        sizer_2.Add(sizer_7, 0, wx.EXPAND | wx.TOP, 10)

        label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, "0")
        label_4.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        sizer_7.Add(label_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)

        sizer_8 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Balance Partida Actual:"), wx.VERTICAL)
        sizer_2.Add(sizer_8, 0, wx.EXPAND | wx.TOP, 10)

        label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, "0")
        label_5.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        sizer_8.Add(label_5, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)

        sizer_9 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, u"Cuenta Atrás:"), wx.VERTICAL)
        sizer_2.Add(sizer_9, 0, wx.EXPAND | wx.TOP, 10)

        label_6 = wx.StaticText(self.panel_1, wx.ID_ANY, "10")
        label_6.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        sizer_9.Add(label_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)

        self.panel_juego = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.panel_juego, 1, wx.EXPAND, 0)

        sizer_10 = wx.BoxSizer(wx.VERTICAL)

        self.panel_croupier = wx.Panel(self.panel_juego, wx.ID_ANY)
        sizer_10.Add(self.panel_croupier, 1, wx.EXPAND, 0)

        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)

        label_7 = wx.StaticText(self.panel_croupier, wx.ID_ANY, "Croupier\n(0)\nActiva")
        label_7.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_11.Add(label_7, 0, 0, 0)

        sizer_11.Add((0, 0), 0, 0, 0)

        self.panel_2_control = wx.Panel(self.panel_croupier, wx.ID_ANY)
        sizer_11.Add(self.panel_2_control, 1, wx.EXPAND, 0)

        self.panel_jugador = wx.Panel(self.panel_juego, wx.ID_ANY)
        sizer_10.Add(self.panel_jugador, 1, wx.EXPAND, 0)

        sizer_jugador = wx.BoxSizer(wx.VERTICAL)

        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_jugador.Add(sizer_12, 1, wx.EXPAND, 0)

        label_8 = wx.StaticText(self.panel_jugador, wx.ID_ANY, "(Valor)\nApuesta\nEstado")
        label_8.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_12.Add(label_8, 0, 0, 0)

        sizer_12.Add((0, 0), 0, 0, 0)

        self.panel_jugador_control = wx.Panel(self.panel_jugador, wx.ID_ANY)
        sizer_12.Add(self.panel_jugador_control, 1, wx.EXPAND, 0)

        self.panel_jugador.SetSizer(sizer_jugador)

        self.panel_croupier.SetSizer(sizer_11)

        self.panel_juego.SetSizer(sizer_10)

        self.panel_1.SetSizer(sizer_1)

        sizer_1.Fit(self)
        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.curiosidad, self.bitmap_button_1)
        self.Bind(wx.EVT_RADIOBUTTON, self.modoManual, self.radio_btn_1)
        self.Bind(wx.EVT_RADIOBUTTON, self.modoAutomatico, self.radio_btn_2)
        self.Bind(wx.EVT_BUTTON, self.accionPedir, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.accionDoblar, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.accionCerrar, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.accionSeparar, self.button_4)
        # end wxGlade

    def curiosidad(self, event):  # wxGlade: automatico.<event_handler>
        print("Event handler 'curiosidad' not implemented!")
        event.Skip()

    def modoManual(self, event):  # wxGlade: automatico.<event_handler>
        print("Event handler 'modoManual' not implemented!")
        event.Skip()

    def modoAutomatico(self, event):  # wxGlade: automatico.<event_handler>
        print("Event handler 'modoAutomatico' not implemented!")
        event.Skip()

    def accionPedir(self, event):  # wxGlade: automatico.<event_handler>
        print("Event handler 'accionPedir' not implemented!")
        event.Skip()

    def accionDoblar(self, event):  # wxGlade: automatico.<event_handler>
        print("Event handler 'accionDoblar' not implemented!")
        event.Skip()

    def accionCerrar(self, event):  # wxGlade: automatico.<event_handler>
        print("Event handler 'accionCerrar' not implemented!")
        event.Skip()

    def accionSeparar(self, event):  # wxGlade: automatico.<event_handler>
        print("Event handler 'accionSeparar' not implemented!")
        event.Skip()

# end of class automatico

class MyApp(wx.App):
    def OnInit(self):
        self.frame = inicio(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
