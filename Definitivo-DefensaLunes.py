'''
Practica 2 BlackJack
Realizada por:
    - Alejandro Garcia Lavandera
    - Angel Antolin
'''

import wx, wx.adv, random  
from externo import CartaBase, Mazo, Estrategia

# Clase que representa las Cartas
class Carta(CartaBase):    
    # Funcion que traduce el indice de la carta en el palo
    @property
    def palo(self):
        if self.ind >= 0 and self.ind <= 12:
            return "♠"  # [PICAS]
        elif self.ind >= 13 and self.ind <= 25:
            return "♣" # [TREBOLES]
        elif self.ind >= 26 and self.ind <= 38:
            return "♥" # [CORAZONES]
        else:
            return "♦" # [DIAMANTES]

    def numero (self):
        return super().valor


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
        
class Mano:
    def __init__(self):
        self.listaCartas = []       # Guardamos los indices de las manos
        self.valorMano = 0          # Valor total de la mano
        self.estadoMano = "Activa"  # Estado de la mano
        self.sizerMano = ""
        self.sizerCartas = ""
        self.texto = ""
        self.boton = ""
    
    def agregarCarta(self, carta):
        self.listaCartas.append(carta)


class Croupier:
    def __init__(self):
        self.manoCroupier = Mano()  # Mano del croupier

class Jugador:
    def __init__(self):
        self.listaManos = []        # Array de Manos
        self.listaApuesta = []      # Apuestas de cada mano
        self.estadosManos = []      # Estados de cada mano
        self.nombreManos = []       # Lista de los nombres de las manos
        

    def agregarCartaJugador(self, indiceMano, carta):
        
        self.listaManos[indiceMano].listaCartas.append(carta)
        
    


class BLACKJACK(wx.Frame):
    

    # Creo el mazo para la partida
    estrategia = Estrategia(Mazo.NUM_BARAJAS)
    mazo = Mazo(Carta, estrategia)
    
    # Variables para los datos de las partidas
    contPartidas = 1        #Número de partidas que se han jugado
    balanceTotal = 0        #Balance total de todas las partidas
    balancePart = 0      #Contador del balance de la partida actual
    
    finPartida = False    
    modoAnalisis = False
    manoActiva = 0
    hayBlackjack = False

    jugador = Jugador()
    croupier = Croupier()
    

    def __init__(self, *args, **kwds):
        # begin wxGlade: BLACKJACK.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("BlackJack")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./media/imgs/icono.jpeg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.Maximize(True)

        self.agregarManoJugador()

        #####################
        ## PANEL BLACKJACK ##
        #####################
        self.panel_blackjack = wx.Panel(self, wx.ID_ANY)

        self.sizer_info_blackjack = wx.BoxSizer(wx.HORIZONTAL)



        ########################
        ## SIZER MENU PARTIDA ##
        ########################
        sizer_menu_partida = wx.BoxSizer(wx.VERTICAL)
        self.sizer_info_blackjack.Add(sizer_menu_partida, 0, wx.EXPAND, 0)



        ##########################
        ## SELECCION MODO JUEGO ##
        ##########################
        sizer_selecModoJuego = wx.StaticBoxSizer(wx.StaticBox(self.panel_blackjack, wx.ID_ANY, "Modo de juego:"), wx.HORIZONTAL)
        sizer_menu_partida.Add(sizer_selecModoJuego, 0, wx.EXPAND, 0)

        self.radioButton_Manual = wx.RadioButton(self.panel_blackjack, wx.ID_ANY, "Manual")
        self.radioButton_Manual.SetValue(1)
        sizer_selecModoJuego.Add(self.radioButton_Manual, 0, 0, 0)

        self.radioButton_Automatico = wx.RadioButton(self.panel_blackjack, wx.ID_ANY, "Automatico")
        sizer_selecModoJuego.Add(self.radioButton_Automatico, 0, 0, 0)



        #########################
        ## RETARDO ANIMACIONES ##
        #########################
        sizer_animaciones_delay = wx.StaticBoxSizer(wx.StaticBox(self.panel_blackjack, wx.ID_ANY, "Delay de las animaciones:"), wx.HORIZONTAL)
        sizer_menu_partida.Add(sizer_animaciones_delay, 0, wx.EXPAND, 0)

        texto_retardoAnimaciones = wx.StaticText(self.panel_blackjack, wx.ID_ANY, "Retardo:")
        sizer_animaciones_delay.Add(texto_retardoAnimaciones, 0, 0, 0)

        self.input_retardoAnimaciones = wx.TextCtrl(self.panel_blackjack, wx.ID_ANY, "25", style=wx.TE_RIGHT)
        sizer_animaciones_delay.Add(self.input_retardoAnimaciones, 0, 0, 0)

        texto_unidadesRetardo = wx.StaticText(self.panel_blackjack, wx.ID_ANY, "ms.")
        sizer_animaciones_delay.Add(texto_unidadesRetardo, 0, 0, 0)
        
        
        
        #######################
        ## SELECCION APUESTA ##
        #######################
        sizer_SeleccionApuestas = wx.StaticBoxSizer(wx.StaticBox(self.panel_blackjack, wx.ID_ANY, "Apuesta:"), wx.VERTICAL)
        sizer_menu_partida.Add(sizer_SeleccionApuestas, 0, wx.EXPAND, 0)

        self.boton_Apuesta2 = wx.Button(self.panel_blackjack, wx.ID_ANY, u"2€")
        sizer_SeleccionApuestas.Add(self.boton_Apuesta2, 0, wx.EXPAND, 0)

        self.boton_Apuesta10 = wx.Button(self.panel_blackjack, wx.ID_ANY, u"10€")
        sizer_SeleccionApuestas.Add(self.boton_Apuesta10, 0, wx.EXPAND, 0)

        self.boton_Apuesta50 = wx.Button(self.panel_blackjack, wx.ID_ANY, u"50€")
        sizer_SeleccionApuestas.Add(self.boton_Apuesta50, 0, wx.EXPAND, 0)


        
        ######################
        ## SELECCION ACCION ##
        ######################
        sizer_Acciones = wx.StaticBoxSizer(wx.StaticBox(self.panel_blackjack, wx.ID_ANY, "Accion:"), wx.VERTICAL)
        sizer_menu_partida.Add(sizer_Acciones, 0, wx.EXPAND, 0)

        self.boton_Pedir = wx.Button(self.panel_blackjack, wx.ID_ANY, "Pedir")
        sizer_Acciones.Add(self.boton_Pedir, 0, wx.EXPAND, 0)

        self.boton_Doblar = wx.Button(self.panel_blackjack, wx.ID_ANY, "Doblar")
        sizer_Acciones.Add(self.boton_Doblar, 0, wx.EXPAND, 0)

        self.boton_Cerrar = wx.Button(self.panel_blackjack, wx.ID_ANY, "Cerrar")
        sizer_Acciones.Add(self.boton_Cerrar, 0, wx.EXPAND, 0)

        self.boton_Separar = wx.Button(self.panel_blackjack, wx.ID_ANY, "Separar")
        sizer_Acciones.Add(self.boton_Separar, 0, wx.EXPAND, 0)
        
        ##########################
        ## CODIGO DEFENSA LUNES ##
        ##########################
        self.boton_Renunciar = wx.Button(self.panel_blackjack, wx.ID_ANY, "Renunciar")
        sizer_Acciones.Add(self.boton_Renunciar, 0, wx.EXPAND, 0)
        
        self.boton_Renunciar.Hide()
        
        
        
        self.boton_Pedir.Hide()
        self.boton_Doblar.Hide()
        self.boton_Cerrar.Hide()
        self.boton_Separar.Hide()

        self.panel_blackjack.Layout()

        ####################
        ## NUMERO PARTIDA ##
        ####################
        sizer_NumPartida = wx.StaticBoxSizer(wx.StaticBox(self.panel_blackjack, wx.ID_ANY, "Numero Partida:"), wx.VERTICAL)
        sizer_menu_partida.Add(sizer_NumPartida, 0, wx.EXPAND, 0)

        self.texto_NumPartida = wx.StaticText(self.panel_blackjack, wx.ID_ANY, "0")
        self.texto_NumPartida.SetFont(wx.Font(22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Arial Rounded MT Bold"))
        sizer_NumPartida.Add(self.texto_NumPartida, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)



        #####################
        ## BALANCE PARTIDA ##
        #####################
        sizer_balancePartida = wx.StaticBoxSizer(wx.StaticBox(self.panel_blackjack, wx.ID_ANY, "Balance Partida:"), wx.VERTICAL)
        sizer_menu_partida.Add(sizer_balancePartida, 0, wx.EXPAND, 0)

        self.texto_BalancePartida = wx.StaticText(self.panel_blackjack, wx.ID_ANY, "0")
        self.texto_BalancePartida.SetFont(wx.Font(22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Arial Rounded MT Bold"))
        sizer_balancePartida.Add(self.texto_BalancePartida, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)



        ####################
        ## BALANCE GLOBAL ##
        ####################
        sizer_BalanceGlobal = wx.StaticBoxSizer(wx.StaticBox(self.panel_blackjack, wx.ID_ANY, "Balance Global:"), wx.VERTICAL)
        sizer_menu_partida.Add(sizer_BalanceGlobal, 0, wx.EXPAND, 0)

        self.texto_BalanceGlobal = wx.StaticText(self.panel_blackjack, wx.ID_ANY, "0")
        self.texto_BalanceGlobal.SetFont(wx.Font(22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Arial Rounded MT Bold"))
        sizer_BalanceGlobal.Add(self.texto_BalanceGlobal, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)
        
        
        
        #####################
        ## TIEMPO RESTANTE ##
        #####################
        sizer_TiempoRestante = wx.StaticBoxSizer(wx.StaticBox(self.panel_blackjack, wx.ID_ANY, "Tiempo Restante:"), wx.VERTICAL)
        sizer_menu_partida.Add(sizer_TiempoRestante, 0, wx.EXPAND, 0)

        self.texto_TiempoRestante = wx.StaticText(self.panel_blackjack, wx.ID_ANY, "10s")
        self.texto_TiempoRestante.SetFont(wx.Font(22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Arial Rounded MT Bold"))
        sizer_TiempoRestante.Add(self.texto_TiempoRestante, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)
        
        self.timer = wx.Timer(self, -1)     # Creamos el objeto timer
        self.cuenta = 10
        self.Bind(wx.EVT_TIMER, self.cuentaRegresiva)  # Enlazo la funcion con el timer




        ####################
        ## VOLVER A JUGAR ##
        ####################
        sizer_VolverJugar = wx.StaticBoxSizer(wx.StaticBox(self.panel_blackjack, wx.ID_ANY, "Volver a jugar:"), wx.VERTICAL)
        sizer_menu_partida.Add(sizer_VolverJugar, 0, wx.EXPAND, 0)

        self.boton_VolverJugarSi = wx.Button(self.panel_blackjack, wx.ID_ANY, "Si")
        sizer_VolverJugar.Add(self.boton_VolverJugarSi, 0, wx.EXPAND, 0)

        self.boton_VolverJugarNo = wx.Button(self.panel_blackjack, wx.ID_ANY, "No")
        sizer_VolverJugar.Add(self.boton_VolverJugarNo, 0, wx.EXPAND, 0)

        self.boton_VolverJugarSi.Hide()
        self.boton_VolverJugarNo.Hide()

        self.panel_blackjack.Layout()
        
        
        
        #########################
        ## MUSICA BOTON BITMAP ##
        #########################
        self.bitmapLuigiDealer = wx.BitmapButton(self.panel_blackjack, wx.ID_ANY, wx.Bitmap("./media/imgs/musica.png", wx.BITMAP_TYPE_ANY))
        self.bitmapLuigiDealer.SetSize(self.bitmapLuigiDealer.GetBestSize())
        sizer_menu_partida.Add(self.bitmapLuigiDealer, 0, 0, 0)

        self.isPlaying = False
        
        self.barajear_gif = wx.adv.Animation()
        self.barajear_gif.LoadFile("./media/imgs/luigiBarajea.gif")

        self.barajear_gif_ctrl = wx.adv.AnimationCtrl(self.panel_blackjack, wx.ID_ANY, self.barajear_gif)
        
        self.repartir_gif = wx.adv.Animation()
        self.repartir_gif.LoadFile("./media/imgs/luigiReparte.gif")

        self.repartir_gif_ctrl = wx.adv.AnimationCtrl(self.panel_blackjack, wx.ID_ANY, self.repartir_gif)

        self.win_gif = wx.adv.Animation()
        self.win_gif.LoadFile("./media/imgs/luigi-you-win.gif")

        self.win_gif_ctrl = wx.adv.AnimationCtrl(self.panel_blackjack, wx.ID_ANY, self.win_gif)
        
        self.bad_gif = wx.adv.Animation()
        self.bad_gif.LoadFile("./media/imgs/luigi-bad.gif")

        self.bad_gif_ctrl = wx.adv.AnimationCtrl(self.panel_blackjack, wx.ID_ANY, self.bad_gif)

        sizer_menu_partida.Add(self.barajear_gif_ctrl, 0, 0, 0)
        sizer_menu_partida.Add(self.repartir_gif_ctrl, 0, 0, 0)
        sizer_menu_partida.Add(self.win_gif_ctrl, 0, 0 ,0)
        sizer_menu_partida.Add(self.bad_gif_ctrl, 0, 0, 0)


        self.barajear_gif_ctrl.Play()
        
        self.repartir_gif_ctrl.Hide()
        self.win_gif_ctrl.Hide()
        self.bad_gif_ctrl.Hide()
        
        #########################
        ## PANEL TABLERO JUEGO ##
        #########################
        self.panel_tableroJuego = wx.ScrolledWindow(self.panel_blackjack, wx.ID_ANY)
        self.panel_tableroJuego.SetScrollRate(20, 20)
        self.panel_tableroJuego.SetBackgroundColour(wx.Colour(35, 142, 35))
        self.sizer_info_blackjack.Add(self.panel_tableroJuego, 1, wx.EXPAND, 0)

        self.sizer_TableroJuego = wx.BoxSizer(wx.VERTICAL)



        ###################
        ## ZONA CROUPIER ##
        ###################
        self.sizer_Croupier = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_TableroJuego.Add(self.sizer_Croupier, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 0)

        self.texto_InfoCroupier = wx.StaticText(self.panel_tableroJuego, wx.ID_ANY, "Croupier\n(Valor)\nEstado", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.texto_InfoCroupier.SetFont(wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.sizer_Croupier.Add(self.texto_InfoCroupier, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

        self.sizer_CroupierCartas = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_Croupier.Add(self.sizer_CroupierCartas, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 0)

        self.sizer_CroupierCartas.Add((0, 0), 0, 0, 0)
        
        

        ##################
        ## ZONA JUGADOR ##
        ##################
        self.panel_ScrolleableJugador = wx.ScrolledWindow(self.panel_tableroJuego, wx.ID_ANY)
        self.panel_ScrolleableJugador.SetScrollRate(10, 10)
        self.sizer_TableroJuego.Add(self.panel_ScrolleableJugador, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 0)

        self.sizer_JugadorManos = wx.BoxSizer(wx.VERTICAL)


        self.jugador.listaManos[0].sizerMano = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_JugadorManos.Add(self.jugador.listaManos[0].sizerMano, 1, wx.EXPAND, 0)
        


        self.jugador.listaManos[0].boton = wx.ToggleButton(self.panel_ScrolleableJugador, 0, f"{self.jugador.nombreManos[0]}")
        self.jugador.listaManos[0].sizerMano.Add(self.jugador.listaManos[0].boton, 0, wx.EXPAND | wx.RIGHT, 10)

        self.jugador.listaManos[0].boton.SetValue(True)

        self.jugador.listaManos[0].boton.SetBackgroundColour(wx.Colour(255, 215, 0))
        

        self.jugador.listaManos[0].texto = wx.StaticText(self.panel_ScrolleableJugador, 0, "Apuesta\n(Valor)\nEstado", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.jugador.listaManos[0].texto.SetFont(wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.jugador.listaManos[0].sizerMano.Add(self.jugador.listaManos[0].texto, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

        self.jugador.listaManos[0].sizerCartas = wx.BoxSizer(wx.HORIZONTAL)
        self.jugador.listaManos[0].sizerMano.Add(self.jugador.listaManos[0].sizerCartas, 1, wx.EXPAND, 0)

        
        #########################
        ## PANEL TABLERO JUEGO ##
        #########################
        self.panel_ScrolleableJugador.SetSizer(self.sizer_JugadorManos)
        
        self.panel_tableroJuego.SetSizer(self.sizer_TableroJuego)

        self.panel_blackjack.SetSizer(self.sizer_info_blackjack)

        self.sizer_info_blackjack.Fit(self)
        self.Layout()

        self.Bind(wx.EVT_RADIOBUTTON, self.modoManual, self.radioButton_Manual)
        self.Bind(wx.EVT_RADIOBUTTON, self.modoAutomatico, self.radioButton_Automatico)
        self.Bind(wx.EVT_BUTTON, self.apuesta2, self.boton_Apuesta2)
        self.Bind(wx.EVT_BUTTON, self.apuesta10, self.boton_Apuesta10)
        self.Bind(wx.EVT_BUTTON, self.apuesta50, self.boton_Apuesta50)
        self.Bind(wx.EVT_BUTTON, self.accionPedir, self.boton_Pedir)
        self.Bind(wx.EVT_BUTTON, self.accionDoblar, self.boton_Doblar)
        self.Bind(wx.EVT_BUTTON, self.accionCerrar, self.boton_Cerrar)
        self.Bind(wx.EVT_BUTTON, self.accionSeparar, self.boton_Separar)
        self.Bind(wx.EVT_BUTTON, self.accionRenunciar, self.boton_Renunciar)
        self.Bind(wx.EVT_BUTTON, self.volverJugarSi, self.boton_VolverJugarSi)
        self.Bind(wx.EVT_BUTTON, self.volverJugarNo, self.boton_VolverJugarNo)
        self.Bind(wx.EVT_BUTTON, self.sonidoAmbiente, self.bitmapLuigiDealer)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.seleccionMano, self.jugador.listaManos[0].boton)
        # end wxGlade
 
    # Funcion que genera todos los bitmaps correspondientes al indice de la carta
    def listaIMGsCartas(self):
        # Generamos un array con todas las imagenes correspondientes a su indice
        self.listaIMG = []
        for carta in range(52):
            img = wx.Bitmap()
            img.LoadFile(f"./media/cartas/{carta:02d}.png")
            self.listaIMG.append(img)
    
    # Funcion que muestra el boton de separar cuadno sea posible
    def separarPosible (self, carta1, carta2):
        # Inicializamos la variable en False para el control del bucle
        separar = False
        
        # Si la carta 1 es igual a la carta 2 (los inds) devolvemos True
        if (carta1.numero() == carta2.numero()):   
            separar = True
            return separar
        
        # En caso contrario, devolvemos False
        else:
            return separar

    # Funcion que realiza el reparto inicial
    def repartoInicial(self):
        
        # Mostramos una animacion indicando que se reparte
        self.repartir_gif_ctrl.Show()   # Se muestra
        self.repartir_gif_ctrl.Play()   # Se inicia
        
        # Ocultamos la animacion
        self.barajear_gif_ctrl.Hide()   
        self.win_gif_ctrl.Hide()
        self.bad_gif_ctrl.Hide()
        
        # Cargamos las imagenes de las cartas
        self.listaIMGsCartas()

        # Reparto Croupier
        # Repartimos una carta al croupier
        self.croupier.manoCroupier.agregarCarta(self.mazo.reparte())
        # Recuperamos el indice de la carta obtenida
        self.indiceCroupier = self.croupier.manoCroupier.listaCartas[0].ind
        
        # CODIGO DEFENSA LUNES ##
        #########################
        # Si la carta repartida es un AS, es decir, valor de mano == 11, mostramos el boton de renunciar
        if self.calcularValorMano(self.croupier.manoCroupier.listaCartas) == 11:
            self.boton_Renunciar.Show()


        # Actualizamos la informacion de la mano del croupeir
        self.texto_InfoCroupier.SetLabel("Croupier\n"+ str(self.calcularValorMano(self.croupier.manoCroupier.listaCartas)) + "\nActiva")                #Actualizar valor cartas
        # Creamos un StaticBitmap correspondiente con la mano del croupier
        carta = wx.StaticBitmap(self.panel_tableroJuego, wx.ID_ANY, self.listaIMG[self.indiceCroupier])                                                #Añade la foto
        # Agregamos la carta a la mano visual del croupier
        self.sizer_CroupierCartas.Add(carta, 0, wx.EXPAND | wx.ALL, 5)

        # Actualizamos la pantalla
        self.panel_tableroJuego.Layout()
        self.panel_blackjack.Layout()
        self.panel_ScrolleableJugador.Layout()

        ##########################
        ## CODIGO DEFENSA LUNES ##
        ##########################
        # Repartimos dos cartas al jugador
        for i in range (1):
            # Agregamos la carta al jugador
            self.jugador.agregarCartaJugador(0, self.mazo.reparte())
            # Recuperamos el indice de la carta
            self.indiceJugador = self.jugador.listaManos[0].listaCartas[i].ind
            # Creamos el staticbitmap correspondiente a la carta del jugador
            carta = wx.StaticBitmap(self.panel_ScrolleableJugador, wx.ID_ANY, self.listaIMG[self.indiceJugador])
            # Agregamos la carta a la mano del jugador en la interfaz 
            self.jugador.listaManos[0].sizerCartas.Add(carta, 0, wx.EXPAND | wx.ALL, 5)
            # Actualizamos la informacion del jugador en la interfaz
            self.jugador.listaManos[0].texto.SetLabel(str(self.jugador.listaApuesta[0]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[0].listaCartas)) + "\n" + self.jugador.estadosManos[0])

        # En caso de que el modo analisis sea verdadero
        if self.modoAnalisis == True:
            
            # Llamamos a la funcion Analisis para jugar en modo automatico
            self.Analisis()
        
        # En caso de que no lo sea
        else:
            # Si la longitud del de las cartas de la mano del jugador es "2" y en caso de que las dos cartas tengan el mismo valor
            if (len(self.jugador.listaManos[0].listaCartas) == 2 and self.separarPosible(self.jugador.listaManos[0].listaCartas[0], self.jugador.listaManos[0].listaCartas[1]) == True):
                # Mostramos el boton de separar
                self.boton_Separar.Show()
                self.panel_blackjack.Layout()
                
            # En caso contrario
            else:
                # Ocultamos el boton de separar
                self.boton_Separar.Hide()
            
            self.panel_blackjack.Layout()
            self.panel_tableroJuego.Layout()   
            self.panel_ScrolleableJugador.Layout()
            
            # Si el valor total de la mano del jugador es igual a 21, es deci, blackjack
            if self.calcularValorMano(self.jugador.listaManos[0].listaCartas) == 21:
                
                # Ocultamos todos los botones
                self.boton_Pedir.Hide()
                self.boton_Doblar.Hide()
                self.boton_Cerrar.Hide()
                self.boton_Separar.Hide()
                
                # Actualizamos el valor de al apuesta
                self.jugador.listaApuesta[0] *= 3/2

                # Mostramos la ventana emergente del "BlackJack"
                vBlackJack = BlackJack(None, wx.ID_ANY, "BLACKJACK")
                vBlackJack.Show()

                # Actualizamos la interfaz
                self.panel_blackjack.Layout()
                self.panel_tableroJuego.Layout()
                self.panel_ScrolleableJugador.Layout()

                # Variable para el control de sonidos
                self.hayBlackjack = True

                # Llamamos a la funcion para que se actualicen los balances
                self.compruebaBalance()

                # Actualizamos la interfaz
                self.panel_blackjack.Layout()
                self.panel_tableroJuego.Layout()
                self.panel_ScrolleableJugador.Layout()

            # En caso de que no haya blackjack
            else:
                # Empezamos el timer de la cuenta atras
                self.timer.Start(1000)
                
                # Actualizamos la interfaz
                self.panel_blackjack.Layout()
                self.panel_tableroJuego.Layout()
                self.panel_ScrolleableJugador.Layout()
            
    #Funcion calcula el valor de la mano
    def calcularValorMano (self, mano):
        # Lleva la cuenta del valor total de la mano que se comprueba
        valorTotal = 0
        # Lleva la cuenta de los ases en la mano
        ases = 0
        #Cuenta los ases y suma todos como si fueran 11 para posteriormente ajustarlos
        for carta in mano:
            valor = carta.numero()
            if (valor == 1):
                ases = ases + 1
                valorTotal = valorTotal + 11
            else:
                valorTotal = valorTotal + valor
        #Mientras el valor sea mayor a 21 o halla algun as, ajusta el valor de los ases a 1
        while (valorTotal > 21 and ases > 0):
            valorTotal = valorTotal - 10
            ases = ases - 1
    
        return valorTotal

    # Funcion para la cuenta atras del timer
    def cuentaRegresiva(self, event):
        # En caso de que la cuenta sea mayor de 0, restamos un segundo y actualizamos la interfaz
        if self.cuenta > 0:
            self.cuenta -= 1        # Restamos 1 en la cuenta
            self.texto_TiempoRestante.SetLabel(str(self.cuenta)+"s")    # Actualizamos la interfaz
            
            # Cambiamos los colores
            if self.cuenta in [4,5,6]:
                self.texto_TiempoRestante.SetForegroundColour(wx.Colour(255, 153, 0))
                self.Layout()
                
            elif self.cuenta in [1,2,3]:
                self.Layout()
                self.texto_TiempoRestante.SetForegroundColour(wx.Colour(255, 0, 0))
                self.Layout()
                
            else:
                self.texto_TiempoRestante.SetForegroundColour(wx.Colour(0, 0, 0))
                self.Layout()
                
            self.Layout()
        
        # En caso de que la cuenta llegue a 0, paramos la cuenta y realizamos para una mano aleatoria, una acciona aleatoria dependiendo del estado de la mano
        elif self.cuenta == 0:
            self.timer.Stop()

            # Realizo una acciona al azar para una mano al azar
            finBucle = True
            while finBucle == True:
                # Eligo una mano al azar
                manoSeleccionada = random.randint(0, len(self.jugador.listaManos) - 1)
                # Compruebo si la mano es valida para editar
                if self.jugador.estadosManos[manoSeleccionada] in ["Cerrada", "Pasada"]:    # La mano no se puede editar
                    manoSeleccionada = random.randint(0, len(self.jugador.listaManos) - 1)     # Vuelvo a elegir otra mano
                
                # Compruebo la cantidad de posibilidades que tiene la mano para jugar 
                elif len(self.jugador.listaManos[manoSeleccionada].listaCartas) == 2 and self.separarPosible(self.jugador.listaManos[manoSeleccionada].listaCartas[0], self.jugador.listaManos[manoSeleccionada].listaCartas[1]):
                    accionAzar = random.randint(0, 3)
                    
                    # Realizamos la accion
                    if accionAzar == 0:
                        self.accionPedir(event)
                    elif accionAzar == 1:
                        self.accionDoblar(event)
                    elif accionAzar == 2:
                        self.accionCerrar(event)
                    else:
                        self.accionSeparar(event)
                
                else:
                    # Elegimos una accion al azar
                    accionAzar = random.randint(0,2)
                    
                    # Realizamos la accion
                    if accionAzar == 0:
                        self.accionPedir(event)
                    elif accionAzar == 1:
                        self.accionDoblar(event)
                    elif accionAzar == 2:
                        self.accionCerrar(event)
                
                # Reiniciamos el contador
                self.cuenta = 10
                self.timer.Stop()
                self.texto_TiempoRestante.SetLabel(str(self.cuenta)+"s")
                self.timer.Start(1000)
                self.Layout()  
                finBucle = False     

        event.Skip()
        
    # Funcion para el modo manual
    def modoManual(self, event):  # wxGlade: BLACKJACK.<event_handler>
        # En caso de querer pasar a modo analisis
        self.modoAnalisis = False
        
        # Establecemos el valor de la apuesta del jugador en 0 
        if (self.jugador.listaApuesta[0] == 0):
            # Mostramos los botones de la apuesta
            self.boton_Apuesta2.Show()
            self.boton_Apuesta10.Show()
            self.boton_Apuesta50.Show()
        # Actualizamos la interfaz
        self.panel_blackjack.Layout()

        event.Skip()
    
    # Funcion para el modo Automatico
    def modoAutomatico(self, event):  # wxGlade: BLACKJACK.<event_handler>
        
        self.modoAnalisis = True
        # Ocultamos los botones de las acciones
        self.boton_Pedir.Hide()
        self.boton_Doblar.Hide()
        self.boton_Cerrar.Hide()
        self.boton_Separar.Hide()
        # En caso de que el valor de la apuesta del jugador sea 0
        if (len(self.jugador.listaApuesta) == 0):
            # Ocultamos los botones de la apuesta
            self.boton_Apuesta2.Hide()
            self.boton_Apuesta10.Hide()
            self.boton_Apuesta50.Hide()
            # Asignamos la apuesta de forma automatica con el archivo externos
            self.jugador.listaApuesta.append(self.estrategia.apuesta(apu_lo = 2, apu_med= 10, apu_hi= 50))
            # Llamamos a la funcion repartoInicial
            self.repartoInicial()
        
        # En caso de que no lo sea
        else:
            # Llamamos a la funcion analisis para que juegue solo
            self.Analisis()
        
        event.Skip()

    # Funcion que gestiona y controla el metodo Automatico
    def Analisis(self):
        # Actualizamos la informacion
        self.panel_blackjack.Layout()
        self.panel_tableroJuego.Layout()
        self.panel_ScrolleableJugador.Layout()
        
        # En caso de que haya blackjack
        if self.calcularValorMano(self.jugador.listaManos[0].listaCartas) == 21:
            
            self.jugador.listaApuesta[0] *= 3/2
            
            vBlackJack = BlackJack(None, wx.ID_ANY, "BLACKJACK")
            vBlackJack.Show()

            self.panel_blackjack.Layout()
            self.panel_tableroJuego.Layout()
            self.panel_ScrolleableJugador.Layout()
            self.hayBlackjack = True
            
            self.compruebaBalance()

            self.panel_blackjack.Layout()
            self.panel_tableroJuego.Layout()
            self.panel_ScrolleableJugador.Layout()
        
        else: 
            
            self.turno = True
            while (self.turno == True):
                # Se realiza una accion para cada mano en las manos del jugador
                for i in range(len(self.jugador.listaManos)):

                    if (self.jugador.estadosManos[i] == "Activa"):

                        jugada = self.estrategia.jugada(self.croupier.manoCroupier.listaCartas[0], self.jugador.listaManos[i].listaCartas)
                        
                        if (jugada == "P"):

                            manoSeleccionada = i
        
                            # Darle una carta al jugador en esa mano
                            self.jugador.agregarCartaJugador(manoSeleccionada, self.mazo.reparte())
                            # Guardo el indice de la carta añadida
                            self.indiceJugador = self.jugador.listaManos[manoSeleccionada].listaCartas[-1].ind
                            # Creo el staticbitmap de la carta
                            carta = wx.StaticBitmap(self.panel_ScrolleableJugador, wx.ID_ANY, self.listaIMG[self.indiceJugador])
        
                            # Metemos la imagen en la mano seleccionada
                            self.jugador.listaManos[manoSeleccionada].sizerCartas.Add(carta, 0, wx.EXPAND | wx.ALL, 5)
                            self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])

                            # Actualizamos
                            self.panel_blackjack.Layout()
                            self.panel_tableroJuego.Layout()
        
                            if self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas) > 21:

                                self.jugador.estadosManos[manoSeleccionada] = "Pasada"
                                self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])
            
                                self.jugador.listaManos[manoSeleccionada].boton.Hide()

                                self.panel_blackjack.Layout()
                                self.panel_tableroJuego.Layout()
                        
                        elif(jugada == "D"):

                            # Tenemos que recoger que mano es la seleccionada con los botones
        
                            manoSeleccionada = i
        
                            # Cambio el estado de la mano a "Cerrada"
                            self.jugador.estadosManos[manoSeleccionada] = "Cerrada"
                            # Darle una carta al jugador en esa mano
                            self.jugador.agregarCartaJugador(manoSeleccionada, self.mazo.reparte())
                            # Guardo el indice de la carta añadida
                            self.indiceJugador = self.jugador.listaManos[manoSeleccionada].listaCartas[-1].ind
                            # Creo el staticbitmap de la carta
                            carta = wx.StaticBitmap(self.panel_ScrolleableJugador, wx.ID_ANY, self.listaIMG[self.indiceJugador])

                            self.jugador.listaApuesta[manoSeleccionada] *= 2
        
                            # Metemos la imagen en la mano seleccionada
                            self.jugador.listaManos[manoSeleccionada].sizerCartas.Add(carta, 0, wx.EXPAND | wx.ALL, 5)
                            self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])
                            self.jugador.listaManos[manoSeleccionada].boton.Hide()
                            # Actualizamos
                            self.panel_blackjack.Layout()
                            self.panel_tableroJuego.Layout()
        
                            if self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas) > 21:

                                self.jugador.estadosManos[manoSeleccionada] = "Pasada"
                                self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])
                                self.jugador.listaManos[manoSeleccionada].boton.Hide()
                                self.panel_blackjack.Layout()
                                self.panel_tableroJuego.Layout()
                        

                        elif(jugada == "C"):

                            # Tenemos que recoger que mano es la seleccionada con los botones
        
                            manoSeleccionada = i
                
                            # Cambiamos el estado de la mano a "Cerrada"
                            self.jugador.estadosManos[manoSeleccionada] = "Cerrada"
                            #  Actualizo la informacion de la mano seleccionada
                            self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])

                            self.jugador.listaManos[manoSeleccionada].boton.Hide()
                            # Actualizamos
                            self.panel_blackjack.Layout()
                            self.panel_tableroJuego.Layout()

                        elif(jugada == "S"):

                            manoSeleccionada = i                                                #Seleccionar la mano
        
                            self.agregarManoJugador()     
        
                            self.crearManoJugador()                                                                  #Agregar una mano
        
                            apuestaMover = self.jugador.listaApuesta[manoSeleccionada]                          #Copiar la apuesta
                                              
        
                            cartaMover = self.jugador.listaManos[manoSeleccionada].listaCartas[-1]          #seleccionar la carta a mover
                            
                            self.jugador.agregarCartaJugador(-1, cartaMover)                                                #Se agrega la carta a la nueva mano
                            
                            self.jugador.listaApuesta.append(apuestaMover)                                                  #Se pone la apuesta
                            
                            self.indiceJugador = self.jugador.listaManos[manoSeleccionada].listaCartas[1].ind               #Se saca el indice de la carta para poder volver a poner la foto
                            

                            del self.jugador.listaManos[manoSeleccionada].listaCartas[-1]
                            
                            self.jugador.listaManos[manoSeleccionada].sizerCartas.Children[-1].Window.Destroy()                                     #Eliminar la foto de la mano
                        

                            carta = wx.StaticBitmap(self.panel_ScrolleableJugador, wx.ID_ANY, self.listaIMG[self.indiceJugador])
                            
                            self.jugador.listaManos[-1].sizerCartas.Add(carta, 0, wx.EXPAND | wx.ALL, 5)
                            
                            self.jugador.listaManos[-1].texto.SetLabel(str(self.jugador.listaApuesta[-1]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[-1].listaCartas)) + "\n" + self.jugador.estadosManos[-1])
                            
                            self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])
                            
                            self.panel_blackjack.Layout()
                            self.panel_tableroJuego.Layout()
                
                
                self.turnoJugador()          
    
    # Apuesta 2 y comienza el repartoInicial                                     
    def apuesta2(self, event):  # wxGlade: BLACKJACK.<event_handler>
        

        self.jugador.listaApuesta.append(2)
        
        self.barajear_gif_ctrl.Stop()
        self.barajear_gif_ctrl.Hide()

        self.boton_Apuesta2.Hide()
        self.boton_Apuesta10.Hide()
        self.boton_Apuesta50.Hide()
        
        self.boton_Pedir.Show()
        self.boton_Doblar.Show()
        self.boton_Cerrar.Show()
        self.boton_Separar.Show()

        
        self.repartoInicial()

        event.Skip()

    # Apuesta 10 y comienza el repartoInicial
    def apuesta10(self, event):  # wxGlade: BLACKJACK.<event_handler>
        
        self.jugador.listaApuesta.append(10)
        
        self.barajear_gif_ctrl.Stop()
        self.barajear_gif_ctrl.Hide()
        
        
        self.boton_Apuesta2.Hide()
        self.boton_Apuesta10.Hide()
        self.boton_Apuesta50.Hide()
        self.boton_Pedir.Show()
        self.boton_Doblar.Show()
        self.boton_Cerrar.Show()
        self.boton_Separar.Show()
        
        self.repartoInicial()
        
        event.Skip()

    # Apuesta 50 y comienza el repartoInicial
    def apuesta50(self, event):  # wxGlade: BLACKJACK.<event_handler>
        
        self.jugador.listaApuesta.append(50)
       
        self.barajear_gif_ctrl.Stop()
        self.barajear_gif_ctrl.Hide()
        
        
        self.boton_Apuesta2.Hide()
        self.boton_Apuesta10.Hide()
        self.boton_Apuesta50.Hide()
        self.boton_Pedir.Show()
        self.boton_Doblar.Show()
        self.boton_Cerrar.Show()
        self.boton_Separar.Show()
        
        self.repartoInicial()
        
        event.Skip()
    
    # Pide una carta para la mano seleccionada del jugador
    def accionPedir(self, event):  # wxGlade: BLACKJACK.<event_handler>
        # Tenemos que recoger que mano es la seleccionada con los botones
        
        manoSeleccionada = self.manoActiva
        
        # Darle una carta al jugador en esa mano
        self.jugador.agregarCartaJugador(manoSeleccionada, self.mazo.reparte())
        # Guardo el indice de la carta añadida
        self.indiceJugador = self.jugador.listaManos[manoSeleccionada].listaCartas[-1].ind
        # Creo el staticbitmap de la carta
        carta = wx.StaticBitmap(self.panel_ScrolleableJugador, wx.ID_ANY, self.listaIMG[self.indiceJugador])
        
        # Metemos la imagen en la mano seleccionada
        self.jugador.listaManos[manoSeleccionada].sizerCartas.Add(carta, 0, wx.EXPAND | wx.ALL, 5)
        self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])

        # Actualizamos
        self.panel_blackjack.Layout()
        self.panel_tableroJuego.Layout()
        
        if self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas) > 21:

            self.jugador.estadosManos[manoSeleccionada] = "Pasada"
            self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])
            
            self.jugador.listaManos[manoSeleccionada].boton.Hide()

            self.panel_blackjack.Layout()
            self.panel_tableroJuego.Layout()
        
        self.turnoJugador()
        
        if self.cuenta != 10:
            self.cuenta = 10
            self.texto_TiempoRestante.SetLabel(str(self.cuenta)+"s")
            self.timer.Start(1000)
            self.Layout()
        
        pop = wx.adv.Sound("./media/sonidos/pop.wav")
        if pop.IsOk():
            pop.Play(wx.adv.SOUND_ASYNC)

        event.Skip()

    # Para la mano seleccionada, dobla la apuesta, pide una carta y cierra la mano
    def accionDoblar(self, event):  # wxGlade: BLACKJACK.<event_handler>
        # Tenemos que recoger que mano es la seleccionada con los botones
        
        manoSeleccionada = self.manoActiva
        
        # Cambio el estado de la mano a "Cerrada"
        self.jugador.estadosManos[manoSeleccionada] = "Cerrada"
        # Darle una carta al jugador en esa mano
        self.jugador.agregarCartaJugador(manoSeleccionada, self.mazo.reparte())
        # Guardo el indice de la carta añadida
        self.indiceJugador = self.jugador.listaManos[manoSeleccionada].listaCartas[-1].ind
        # Creo el staticbitmap de la carta
        carta = wx.StaticBitmap(self.panel_ScrolleableJugador, wx.ID_ANY, self.listaIMG[self.indiceJugador])

        self.jugador.listaApuesta[manoSeleccionada] *= 2
        
        # Metemos la imagen en la mano seleccionada
        self.jugador.listaManos[manoSeleccionada].sizerCartas.Add(carta, 0, wx.EXPAND | wx.ALL, 5)
        self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])
        self.jugador.listaManos[manoSeleccionada].boton.Hide()
        # Actualizamos
        self.panel_blackjack.Layout()
        self.panel_tableroJuego.Layout()
        
        if self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas) > 21:

            self.jugador.estadosManos[manoSeleccionada] = "Pasada"
            self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])
            self.jugador.listaManos[manoSeleccionada].boton.Hide()
            self.panel_blackjack.Layout()
            self.panel_tableroJuego.Layout()
        
        self.turnoJugador()
        if self.cuenta != 10:
            self.cuenta = 10
            self.texto_TiempoRestante.SetLabel(str(self.cuenta)+"s")
            self.timer.Start(1000)
            self.Layout()
        
        pop = wx.adv.Sound("./media/sonidos/pop.wav")
        if pop.IsOk():
            pop.Play(wx.adv.SOUND_ASYNC)
        event.Skip()

    # Cierra la mano seleccionada
    def accionCerrar(self, event):  # wxGlade: BLACKJACK.<event_handler>
       # Tenemos que recoger que mano es la seleccionada con los botones
        
        manoSeleccionada = self.manoActiva
                
        # Cambiamos el estado de la mano a "Cerrada"
        self.jugador.estadosManos[manoSeleccionada] = "Cerrada"
        # Actualizo la informacion de la mano seleccionada
        self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])

        self.jugador.listaManos[manoSeleccionada].boton.Hide()
        # Actualizamos
        self.panel_blackjack.Layout()
        self.panel_tableroJuego.Layout() 
        
        self.turnoJugador()
        if self.cuenta != 10:
            self.cuenta = 10
            self.texto_TiempoRestante.SetLabel(str(self.cuenta)+"s")
            self.timer.Start(1000)
            self.Layout()
        pop = wx.adv.Sound("./media/sonidos/pop.wav")
        if pop.IsOk():
            pop.Play(wx.adv.SOUND_ASYNC)
        
        event.Skip()

    # Para la mano seleccionada, separa la mano en otra y divide las cartas (solo si son del mismo valor)
    def accionSeparar(self, event):  # wxGlade: BLACKJACK.<event_handler>

        manoSeleccionada = self.manoActiva                                                  #Seleccionar la mano
        
        self.agregarManoJugador()     
        
        self.crearManoJugador()                                                                  #Agregar una mano
        
        apuestaMover = self.jugador.listaApuesta[manoSeleccionada]                          #Copiar la apuesta
                                              
        
        cartaMover = self.jugador.listaManos[manoSeleccionada].listaCartas[-1]          #seleccionar la carta a mover
        
        self.jugador.agregarCartaJugador(-1, cartaMover)                                                #Se agrega la carta a la nueva mano
        
        self.jugador.listaApuesta.append(apuestaMover)                                                  #Se pone la apuesta
        
        self.indiceJugador = self.jugador.listaManos[manoSeleccionada].listaCartas[1].ind               #Se saca el indice de la carta para poder volver a poner la foto
        

        del self.jugador.listaManos[manoSeleccionada].listaCartas[-1]
        
        self.jugador.listaManos[manoSeleccionada].sizerCartas.Children[-1].Window.Destroy()                                     #Eliminar la foto de la mano
       

        carta = wx.StaticBitmap(self.panel_ScrolleableJugador, wx.ID_ANY, self.listaIMG[self.indiceJugador])
        
        self.jugador.listaManos[-1].sizerCartas.Add(carta, 0, wx.EXPAND | wx.ALL, 5)
        
        self.jugador.listaManos[-1].texto.SetLabel(str(self.jugador.listaApuesta[-1]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[-1].listaCartas)) + "\n" + self.jugador.estadosManos[-1])
        
        self.jugador.listaManos[manoSeleccionada].texto.SetLabel(str(self.jugador.listaApuesta[manoSeleccionada]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[manoSeleccionada].listaCartas)) + "\n" + self.jugador.estadosManos[manoSeleccionada])
        
        self.panel_blackjack.Layout()
        self.panel_tableroJuego.Layout()
        
        self.turnoJugador()
        if self.cuenta != 10:
            self.cuenta = 10
            self.texto_TiempoRestante.SetLabel(str(self.cuenta)+"s")
            self.timer.Start(1000)
            self.Layout()
       
        pop = wx.adv.Sound("./media/sonidos/pop.wav")
        if pop.IsOk():
            pop.Play(wx.adv.SOUND_ASYNC)
        
        event.Skip()

    ## CODIGO DEFENSA LUNES ##
    ##########################
    def accionRenunciar(self, event):
        # Para todas las manos
        for i in range(len(self.jugador.listaManos)):
            self.jugador.estadosManos[i] = "Renunciada"
            self.jugador.listaManos[i].texto.SetLabel(str(self.jugador.listaApuesta[i]) + "€\n" + str(self.calcularValorMano(self.jugador.listaManos[i].listaCartas)) + "\n" + self.jugador.estadosManos[i])
        
        self.Layout()
        
        for i in range(len(self.jugador.listaApuesta)):
            self.jugador.listaApuesta[i] /= 2
        
        self.compruebaBalance()
        pass
    # Funcion para volver a jugar, reinicia todo 
    def volverJugarSi(self, event):  # wxGlade: BLACKJACK.<event_handler>
        
        self.boton_VolverJugarSi.Hide()
        self.boton_VolverJugarNo.Hide()
        self.panel_blackjack.Layout() 
        
        self.contPartidas += 1
        self.hayBlackjack = False
        
        self.texto_NumPartida.SetLabel(f"{str(self.contPartidas)}")

        self.texto_NumPartida.Refresh()

        self.reiniciarPartida()
        
        if self.modoAnalisis == False:

            self.boton_Apuesta2.Show()
            self.boton_Apuesta10.Show()
            self.boton_Apuesta50.Show()
            
            self.panel_blackjack.Layout()
        
        else: 
            
            self.jugador.listaApuesta.append(self.estrategia.apuesta(apu_lo= 2, apu_med= 10, apu_hi= 50))
            self.panel_blackjack.Layout()
            self.panel_tableroJuego.Layout()
            self.panel_ScrolleableJugador.Layout()
            self.repartoInicial()

        self.cuenta = 10
        self.timer.Stop()
        self.texto_TiempoRestante.SetLabel(str(self.cuenta)+"s")
        self.panel_blackjack.Layout()
        self.Layout()  

            
        self.Layout()

        event.Skip()

    # Funcion para salir del juego
    def volverJugarNo(self, event):  # wxGlade: BLACKJACK.<event_handler>
        
        exit()

    # Deja todo preparado para volver a jugar otra partida
    def reiniciarPartida (self):
        
        self.panel_tableroJuego.Destroy()
        self.Layout()
        
        self.jugador = Jugador()
        self.croupier = Croupier()
        self.manoActiva = 0

        self.crearChildren()
    
    # Para volver a jugar, crea todo como el inicio
    def crearChildren(self):
        

        self.agregarManoJugador()

        #########################
        ## PANEL TABLERO JUEGO ##
        #########################
        self.panel_tableroJuego = wx.ScrolledWindow(self.panel_blackjack, wx.ID_ANY)
        self.panel_tableroJuego.SetScrollRate(20, 20)
        self.panel_tableroJuego.SetBackgroundColour(wx.Colour(35, 142, 35))
        self.sizer_info_blackjack.Add(self.panel_tableroJuego, 1, wx.EXPAND, 0)

        self.sizer_TableroJuego = wx.BoxSizer(wx.VERTICAL)
        ###################
        ## ZONA CROUPIER ##
        ###################
        self.sizer_Croupier = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_TableroJuego.Add(self.sizer_Croupier, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 0)

        self.texto_InfoCroupier = wx.StaticText(self.panel_tableroJuego, wx.ID_ANY, "Croupier\n(Valor)\nEstado", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.texto_InfoCroupier.SetFont(wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.sizer_Croupier.Add(self.texto_InfoCroupier, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

        self.sizer_CroupierCartas = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_Croupier.Add(self.sizer_CroupierCartas, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 0)

        self.sizer_CroupierCartas.Add((0, 0), 0, 0, 0)

        ##################
        ## ZONA JUGADOR ##
        ##################
        self.panel_ScrolleableJugador = wx.ScrolledWindow(self.panel_tableroJuego, wx.ID_ANY)
        self.panel_ScrolleableJugador.SetScrollRate(10, 10)
        self.sizer_TableroJuego.Add(self.panel_ScrolleableJugador, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 0)

        self.sizer_JugadorManos = wx.BoxSizer(wx.VERTICAL)


        self.jugador.listaManos[0].sizerMano = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_JugadorManos.Add(self.jugador.listaManos[0].sizerMano, 1, wx.EXPAND, 0)
        


        self.jugador.listaManos[0].boton = wx.ToggleButton(self.panel_ScrolleableJugador, 0, f"{self.jugador.nombreManos[0]}")
        self.jugador.listaManos[0].sizerMano.Add(self.jugador.listaManos[0].boton, 0, wx.EXPAND | wx.RIGHT, 10)

        self.jugador.listaManos[0].boton.SetValue(True)

        self.jugador.listaManos[0].boton.SetBackgroundColour(wx.Colour(255, 215, 0))
        

        self.jugador.listaManos[0].texto = wx.StaticText(self.panel_ScrolleableJugador, 0, "Apuesta\n(Valor)\nEstado", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.jugador.listaManos[0].texto.SetFont(wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.jugador.listaManos[0].sizerMano.Add(self.jugador.listaManos[0].texto, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

        self.jugador.listaManos[0].sizerCartas = wx.BoxSizer(wx.HORIZONTAL)
        self.jugador.listaManos[0].sizerMano.Add(self.jugador.listaManos[0].sizerCartas, 1, wx.EXPAND, 0)

        #########################
        ## PANEL TABLERO JUEGO ##
        #########################
        self.panel_ScrolleableJugador.SetSizer(self.sizer_JugadorManos)
        
        self.panel_tableroJuego.SetSizer(self.sizer_TableroJuego)

        self.panel_blackjack.SetSizer(self.sizer_info_blackjack)

        self.panel_blackjack.Layout()

    # Activa y desactiva el boton de la musica del ambiente
    def sonidoAmbiente(self, event):  # wxGlade: BLACKJACK.<event_handler>
        sound = wx.adv.Sound("./media/sonidos/luigiMusica.wav")
        if self.isPlaying:
            wx.adv.Sound.Stop()
            self.isPlaying = False
        else:
            if sound.IsOk():
                sound.Play(wx.adv.SOUND_ASYNC)
                self.isPlaying = True
        
        event.Skip()

    # Funcion para identificar una mano a la hora de realizar acciones
    def seleccionMano(self, event):  # wxGlade: BLACKJACK.<event_handler>
        
        ident = event.Id

        self.manoActiva = ident

        for i in range (len(self.jugador.listaManos)):

            if self.jugador.listaManos[i].boton.GetId() != ident:
                
                self.jugador.listaManos[i].boton.SetBackgroundColour(wx.Colour(128, 128, 128))

            else:

                self.jugador.listaManos[i].boton.SetBackgroundColour(wx.Colour(255, 215, 0))

        event.Skip()

    # Agrega la mano a la lista de manos del jugador 
    def agregarManoJugador(self):
        # Creo la nueva mano y su nombre
        nuevaMano = Mano()
        nombreMano = f"Mano{chr(ord('A') + len(self.jugador.listaManos))}"
        estadoMano = "Activa"
        
        # Agrego la mano tanto en la lista de las manos como su nombre
        self.jugador.nombreManos.append(nombreMano)
        self.jugador.estadosManos.append(estadoMano)
        self.jugador.listaManos.append(nuevaMano) 

    # Agrega la interfaz a la mano creada
    def crearManoJugador(self):

        self.jugador.listaManos[-1].sizerMano = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_JugadorManos.Add(self.jugador.listaManos[-1].sizerMano, 1, wx.EXPAND, 0)

        self.jugador.listaManos[-1].boton = wx.ToggleButton(self.panel_ScrolleableJugador, len(self.jugador.listaManos) - 1, f"{self.jugador.nombreManos[-1]}")
        self.jugador.listaManos[-1].sizerMano.Add(self.jugador.listaManos[-1].boton, 0, wx.EXPAND | wx.RIGHT, 10)
        self.jugador.listaManos[-1].boton.SetBackgroundColour(wx.Colour(128, 128, 128))


        self.jugador.listaManos[-1].texto = wx.StaticText(self.panel_ScrolleableJugador, len(self.jugador.listaManos) - 1, "Apuesta\n(Valor)\nEstado", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.jugador.listaManos[-1].texto.SetFont(wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        self.jugador.listaManos[-1].sizerMano.Add(self.jugador.listaManos[-1].texto, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

        self.jugador.listaManos[-1].sizerCartas = wx.BoxSizer(wx.HORIZONTAL)
        self.jugador.listaManos[-1].sizerMano.Add(self.jugador.listaManos[-1].sizerCartas, 1, wx.EXPAND, 0)

        self.panel_blackjack.Layout()
        self.panel_tableroJuego.Layout()
        
        self.Bind(wx.EVT_TOGGLEBUTTON, self.seleccionMano, self.jugador.listaManos[-1].boton)

      # Funcion que realiza el turno del croupier
    
    # Turno del croupier (pide hasta que el valor sea >= 17)
    def turnoCroupier(self):
        
        self.timer.Stop()
        self.cuenta = 10
        self.texto_TiempoRestante.SetLabel("10s")
        self.texto_TiempoRestante.SetForegroundColour(wx.Colour(0, 0, 0))
        self.Layout()
        
        self.boton_Pedir.Hide()
        self.boton_Doblar.Hide()
        self.boton_Cerrar.Hide()
        self.boton_Separar.Hide()
        self.boton_Renunciar.Hide()

        self.panel_blackjack.Layout()

        if self.finPartida == False:
            # Pido cartas hasta que el valor total de la mano del croupier > 17
            while self.calcularValorMano(self.croupier.manoCroupier.listaCartas) <= 17:
            

                # Reparto Croupier
                self.croupier.manoCroupier.agregarCarta(self.mazo.reparte())                    #Repartir carta al croupier
                
                
            for i in range (len(self.croupier.manoCroupier.listaCartas)):
                
                if i != 0:
                    indiceCroupier = self.croupier.manoCroupier.listaCartas[i].ind            #Sacar el indice
                
                    self.texto_InfoCroupier.SetLabel("Croupier\n"+ str(self.calcularValorMano(self.croupier.manoCroupier.listaCartas)) + "\nActiva")                #Actualizar valor cartas

                    carta = wx.StaticBitmap(self.panel_tableroJuego, wx.ID_ANY, self.listaIMG[indiceCroupier])                                                #Añade la foto

                    self.sizer_CroupierCartas.Add(carta, 0, wx.EXPAND | wx.ALL, 5)

                    # Actualizamos la pantalla
                    self.panel_tableroJuego.Layout()
                    self.panel_blackjack.Layout
                    self.panel_ScrolleableJugador.Layout()
                    self.Layout()
            
            if self.calcularValorMano(self.croupier.manoCroupier.listaCartas) > 21:

                self.croupier.manoCroupier.estadoMano = "Pasada"
                self.texto_InfoCroupier.SetLabel("Croupier\n"+ str(self.calcularValorMano(self.croupier.manoCroupier.listaCartas)) +"\n" + str(self.croupier.manoCroupier.estadoMano))
                self.panel_blackjack.Layout()
                self.panel_tableroJuego.Layout()
                self.compruebaBalance()
            
            else: 
            
                self.croupier.manoCroupier.estadoMano = "Cerrada"
                self.texto_InfoCroupier.SetLabel("Croupier\n"+ str(self.calcularValorMano(self.croupier.manoCroupier.listaCartas)) +"\n" + str(self.croupier.manoCroupier.estadoMano))
                self.panel_blackjack.Layout()
                self.panel_tableroJuego.Layout()
                self.compruebaBalance() 
        else:

            self.compruebaBalance()  

    # Comprueba si tiene manos activas para poder seguir jugando, en caso contrario, llama al turno del croupier
    def turnoJugador(self):
        # Contamos las manos "bloqueadas"
        manosPasadas = 0
        manosCerradas = 0
        
        # Recorro las manos del jugador
        for i in range(len(self.jugador.listaManos)):
            # Si la mano esta cerrada o pasada +1 manosBloq
            if self.jugador.estadosManos[i] == "Cerrada":
                manosCerradas += 1
            elif self.jugador.estadosManos[i] == "Pasada":
                manosPasadas += 1
                
            # Si todas las manos estan cerradas y/o pasadas, damos paso al croupier
            if manosPasadas == len(self.jugador.listaManos):
                
                self.turno = False
                self.finPartida = True
                self.turnoCroupier()
                
            
            # Si las manos estan pasadas, finalizamos la partida
            elif manosCerradas + manosPasadas == len(self.jugador.listaManos):
                
                self.turno = False
                self.finPartida = False
                self.turnoCroupier()
            
            else:
                pass
            
        self.timer.Stop()
        self.cuenta = 10
        self.texto_TiempoRestante.SetLabel("10s")
        self.texto_TiempoRestante.SetForegroundColour(wx.Colour(0, 0, 0))
        self.Layout()
            
    # Funcion para comprobar el balance general
    def compruebaBalance(self):
        self.boton_VolverJugarSi.Show()
        self.boton_VolverJugarNo.Show()
        
        self.balancePartida()
        self.balanceGlobal() 

        self.boton_Renunciar.Hide()
        
        self.panel_blackjack.Layout()     
        
        self.timer.Stop()
        self.cuenta = 10
        self.texto_TiempoRestante.SetLabel("10s")
        self.texto_TiempoRestante.SetForegroundColour(wx.Colour(0, 0, 0))
        self.Layout()

    # Funcion que controla el balance de la partida
    def balancePartida(self):
        
        balancePart = 0
        
        # Almaceno el valor total de la mano del croupier
        resultadoCroupier = self.calcularValorMano(self.croupier.manoCroupier.listaCartas)
        
        # Almaceno los valores totales de las manos del jugador
        for i in range(len(self.jugador.listaManos)):
            
            resultadoJugador = self.calcularValorMano(self.jugador.listaManos[i].listaCartas)
            
            # Realizo las comprobaciones
            if resultadoJugador > 21:
                
                balancePart += int(self.jugador.listaApuesta[i] * -1)
                self.jugador.listaManos[i].boton.Show()
                self.jugador.listaManos[i].boton.SetBackgroundColour(wx.Colour(255,0,0))
                self.panel_tableroJuego.Layout()

            elif resultadoCroupier > 21 and resultadoJugador <= 21:
                
                balancePart += int(self.jugador.listaApuesta[i])
                self.jugador.listaManos[i].boton.Show()
                self.jugador.listaManos[i].boton.SetBackgroundColour(wx.Colour(29,117,9))
                self.panel_tableroJuego.Layout()
            
            elif resultadoJugador <= 21 and resultadoJugador > resultadoCroupier:
                
                balancePart += int(self.jugador.listaApuesta[i])
                self.jugador.listaManos[i].boton.Show()
                self.jugador.listaManos[i].boton.SetBackgroundColour(wx.Colour(29,117,9))
                self.panel_tableroJuego.Layout()
            
            elif resultadoJugador == resultadoCroupier:
                
                balancePart += 0
                self.jugador.listaManos[i].boton.Show()
                self.jugador.listaManos[i].boton.SetBackgroundColour(wx.Colour(128, 128, 128))
                self.panel_tableroJuego.Layout()
                
            elif resultadoJugador < 21 and resultadoJugador < resultadoCroupier:
                
                balancePart += int(self.jugador.listaApuesta[i] * -1)
                self.jugador.listaManos[i].boton.Show()
                self.jugador.listaManos[i].boton.SetBackgroundColour(wx.Colour(255,0,0))
                self.panel_tableroJuego.Layout()
        # Establezco el color del texto
        if balancePart < 0:
            balanceNegativo = wx.adv.Sound("./media/sonidos/balanceNegativo.wav")
            if balanceNegativo.IsOk():
                balanceNegativo.Play(wx.adv.SOUND_ASYNC)
            self.texto_BalancePartida.SetLabel(f"{balancePart}"+"€")
            self.texto_BalancePartida.SetForegroundColour(wx.Colour(255, 0, 0))
            
            self.bad_gif_ctrl.Show()
            self.bad_gif_ctrl.Play()
            
            self.barajear_gif_ctrl.Hide()
            self.win_gif_ctrl.Hide()
            self.repartir_gif_ctrl.Hide()
            self.repartir_gif_ctrl.Stop()
            self.panel_blackjack.Layout()
        
        elif balancePart == 0:
            balanceNegativo = wx.adv.Sound("./media/sonidos/balanceNegativo.wav")
            if balanceNegativo.IsOk():
                balanceNegativo.Play(wx.adv.SOUND_ASYNC)
            
            self.texto_BalancePartida.SetLabel(f"{balancePart}"+"€")
            self.texto_BalancePartida.SetForegroundColour(wx.Colour(0, 0, 0))
            
            self.bad_gif_ctrl.Show()
            self.bad_gif_ctrl.Play()
            
            self.barajear_gif_ctrl.Hide()
            self.win_gif_ctrl.Hide()
            self.repartir_gif_ctrl.Hide()
            self.repartir_gif_ctrl.Stop()
            self.panel_blackjack.Layout()


        elif balancePart > 0:
            if self.hayBlackjack == False:
                balancePostivo = wx.adv.Sound("./media/sonidos/balancePositivo.wav")
                if balancePostivo.IsOk():
                    balancePostivo.Play(wx.adv.SOUND_ASYNC)
            self.texto_BalancePartida.SetLabel(f"{balancePart}"+"€")
            self.texto_BalancePartida.SetForegroundColour(wx.Colour(0, 255, 0))

            self.win_gif_ctrl.Show()
            self.win_gif_ctrl.Play()
            
            self.barajear_gif_ctrl.Hide()
            self.bad_gif_ctrl.Hide()
            self.repartir_gif_ctrl.Hide()
            self.repartir_gif_ctrl.Stop()
            self.panel_blackjack.Layout()


        self.Layout()
    
        return balancePart   
    
    # Funcion que controla el balance global
    def balanceGlobal(self):
        
        self.balanceTotal += self.balancePartida()
        
        # Establezco el color del texto
        if self.balanceTotal < 0:
            self.texto_BalanceGlobal.SetLabel(f"{self.balanceTotal}"+"€")
            self.texto_BalanceGlobal.SetForegroundColour(wx.Colour(255, 0, 0))
            
        elif self.balanceTotal == 0:
            self.texto_BalanceGlobal.SetLabel(f"{self.balanceTotal}"+"€")
            self.texto_BalanceGlobal.SetForegroundColour(wx.Colour(0, 0, 0))
            
        elif self.balanceTotal > 0:
            self.texto_BalanceGlobal.SetLabel(f"{self.balanceTotal}"+"€")
            self.texto_BalanceGlobal.SetForegroundColour(wx.Colour(0, 255, 0))
        
        self.Layout()
# end of class BLACKJACK

class ATENCION(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ATENCION.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((627, 220))
        self.SetTitle("AVISO")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./media/imgs/icono.jpeg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetBackgroundColour(wx.Colour(0, 255, 0))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, u"¿Cómo empezar a jugar?", style=wx.ALIGN_CENTER_HORIZONTAL)
        label_1.SetBackgroundColour(wx.Colour(0, 255, 0))
        label_1.SetFont(wx.Font(30, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Arial"))
        label_1.SetFocus()
        sizer_1.Add(label_1, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 20)

        label_2 = wx.StaticText(self, wx.ID_ANY, "Manual: Selecciona una apuesta.")
        label_2.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        sizer_1.Add(label_2, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
        sizer_2.AddButton(self.button_CLOSE)

        sizer_2.Realize()

        self.SetSizer(sizer_1)

        self.SetEscapeId(self.button_CLOSE.GetId())

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.cerrarAVISO, self.button_CLOSE)
        # end wxGlade

    def cerrarAVISO(self, event):  # wxGlade: ATENCION.<event_handler>
        self.Hide()
        event.Skip()

# end of class ATENCION

class BlackJack(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: BlackJack.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle("ENHORABUENA")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("./media/imgs/icono.jpeg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        
        self.Center()
        

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("./media/sonidos/blackjack.jpg", wx.BITMAP_TYPE_ANY))
        sizer_1.Add(bitmap_1, 0, 0, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.button_CLOSE = wx.Button(self, wx.ID_CLOSE, "")
        sizer_2.AddButton(self.button_CLOSE)

        sizer_2.Realize()

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.SetEscapeId(self.button_CLOSE.GetId())

        sonido = wx.adv.Sound("./media/sonidos/blackjack.wav")
        if sonido.IsOk():
            sonido.Play(wx.adv.SOUND_ASYNC)
        
        self.Layout()
        # end wxGlade

# end of class BlackJack

class MyApp(wx.App):
    def OnInit(self):
        self.vBlackJack = BLACKJACK(None, wx.ID_ANY, "")
        self.SetTopWindow(self.vBlackJack)
        self.vBlackJack.Show()

        sonido = wx.adv.Sound("./media/sonidos/luigiVoz.wav")
        if sonido.IsOk():
            sonido.Play(wx.adv.SOUND_ASYNC) 
       
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()