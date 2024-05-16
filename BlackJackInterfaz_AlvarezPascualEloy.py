'''
Práctica realizada por Eloy Álvarez Pascual
Grupo: T3. Subgrupo de laboratorio: Z9
'''

'''
EXPLICACIÓN DEL FUNCIONAMIENTO EN MODO JUEGO
Al elegir la apuesta empezará el juego. 
Para realizar una jugada, primero se selecciona la mano con la que se quiere jugar pulsando uno de los botones a la izquierda de cada mano, 
    entonces se mostrarán las jugadas posibles abajo.
Cuando la partida termine, aparecerá la opción de jugar otra vez.
'''

import wx
import time
from externo import Mazo, Estrategia, CartaBase


#Objeto carta
class Carta (CartaBase):
    
    #Atributo palo de la carta
    palo = ''

    def representaCarta(self, carta): #Representa la apariencia de la carta. Tipo Delouxe
        '''
        Asigna el palo y el valor facial de la carta
        Entrada: el objeto carta
        '''

        valorFacial = '' #Valor que se ve en pantalla al mostrar la carta
        indiceCarta = carta.ind #Sirve para saber la figura de la carta, en el caso de que el valor de esta sea 10

        #Asignación del palo de la carta según su índice
        if carta.ind >= 0 and carta.ind <= 13:
            carta.palo = '♠'
        elif carta.ind >= 14 and carta.ind <= 27:
            carta.palo = '♥'
        elif carta.ind >= 28 and carta.ind <= 41:
            carta.palo = '♣'
        elif carta.ind >= 42 and carta.ind <= 51:
            carta.palo = '♦'

        #Asignación del valor facial de la carta
        if carta.valor == 1:
            valorFacial = 'A'
        else:
            valorFacial = carta.valor

        if valorFacial == 10:

            while indiceCarta - 13 > 0:
                indiceCarta -= 13

            if indiceCarta == 10:
                valorFacial = 'J'
            elif indiceCarta == 11:
                valorFacial = 'Q'
            elif indiceCarta == 12:
                valorFacial = 'K'

class Mano:
    #Clase que representa a cada mano

    def __init__(self):

        self.cartas = [] #Las cartas que están contenidas en la mano
        self.nombre = 'Mano'
        self.valor = 0 #El valor total que tiene la mano
        self.estado = 'Activa'
        self.apuesta = 0
        self.manoSizer = '' #Donde se encuentra la mano en la ventana
        self.panel = '' #Donde se encuentra la mano en la ventana
        self.cartasSizer = '' #Donde se encuentran las cartas de la mano en la ventana
        self.cartasVisuales = [] #Almacena las cartas de la mano que se ven en la ventana
        self.infoMano = '' #Información a la izquierda de la mano
        self.botonMano = '' #Botón para seleccionar la mano para realizar una jugada

    def valorYEstado(self, mano):
        '''
        Método para actualizar el valor y el estado de la mano
        Entrada: el objeto mano
        '''
        mano.valor = 0

        for i in mano.cartas:
            mano.valor += i.valor
            
        for i in mano.cartas:
            if i.valor == 1 and mano.valor <= 11:
                mano.valor += 10

        if mano.valor < 21 and mano.estado != 'Pasada' and mano.estado != 'Cerrada':
            mano.estado = 'Activa'
        elif mano.valor > 21:
            mano.estado = 'Pasada'
        elif mano.valor == 21 or mano.estado == 'Cerrada':
            mano.estado = 'Cerrada'

class Variables:
    #Variables ("globales") que se utilizan a lo largo del código

    def setVariables(self):
        '''
        Método que inicializa todas las variables
        '''

        self.jugador = [Mano()] #Almacena las manos del Jugador
        self.croupier = Mano() #Mano del Croupier

        self.finPartida = False #Para saber cúando ha acabado la partida
        self.finJugador = False #Para saber cuándo acaba el turno del Jugador
        self.turnoCroupier = True #Para saber si es turno del croupier

        self.modoPartida = '' #Modo en el que se juega la partida

        self.manoSeleccionada = 0 #Para saber qué mano se ha seleccionado mediante su respectivo botón


class BlackJackInterfaz(wx.Frame):

    #Objeto para acceder a las variables del funcionamiento
    variables=Variables()
    variables.setVariables()

    #Inicio de las clases de externo.py
    estrategia = Estrategia(2)
    mazo = Mazo(Carta, estrategia)

    contPartidas = 1 #Número de partidas que se han jugado
    balanceTotal = 0 #Balance total de todas las partidas
    balancePartida = 0 #Contador del balance de la partida actual

    def __init__(self, *args, **kwds):
        # begin wxGlade: BlackJackInterfaz.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1200, 700))
        self.SetTitle("BlackJack")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("iconoBJ.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetBackgroundColour(wx.Colour(22, 89, 22))

        ####################################################################
        ####################################################################

        AplicacionSizer = wx.BoxSizer(wx.HORIZONTAL)

        InformacionSizer = wx.BoxSizer(wx.VERTICAL)
        AplicacionSizer.Add(InformacionSizer, 1, wx.EXPAND, 0)

        informacionText = wx.StaticText(self, wx.ID_ANY, "\nINFORMACION\n", style=wx.ALIGN_CENTER_HORIZONTAL)
        informacionText.SetMinSize((350, 50))
        informacionText.SetBackgroundColour(wx.Colour(255, 255, 200))
        InformacionSizer.Add(informacionText, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 2)

        practicaText = wx.StaticText(self, wx.ID_ANY, "\n*** PRACTICA 2 - BLACKJACK CON INTERFAZ GRAFICA ***\nEloy Alvarez Pascual\n", style=wx.ALIGN_CENTER_HORIZONTAL)
        practicaText.SetMinSize((350, 60))
        practicaText.SetBackgroundColour(wx.Colour(253, 249, 196))
        InformacionSizer.Add(practicaText, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)

        ####################################################################

        modoPartidaText = wx.StaticText(self, wx.ID_ANY, "\nMODO DE LA PARTIDA\n", style=wx.ALIGN_CENTER_HORIZONTAL)
        modoPartidaText.SetMinSize((350, 50))
        modoPartidaText.SetBackgroundColour(wx.Colour(253, 249, 196))
        InformacionSizer.Add(modoPartidaText, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 1)

        self.modoPartidaChoice = wx.Choice(self, wx.ID_ANY, choices=["Juego", "Automatico"])
        self.modoPartidaChoice.SetMinSize((350, 25))
        self.modoPartidaChoice.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.modoPartidaChoice.SetSelection(0)
        InformacionSizer.Add(self.modoPartidaChoice, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        ####################################################################

        apuestaPartidaText = wx.StaticText(self, wx.ID_ANY, "\nAPUESTA", style=wx.ALIGN_CENTER_HORIZONTAL)
        apuestaPartidaText.SetMinSize((350, 50))
        apuestaPartidaText.SetBackgroundColour(wx.Colour(253, 249, 196))
        InformacionSizer.Add(apuestaPartidaText, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        apuestaPartdaSizer = wx.BoxSizer(wx.HORIZONTAL)
        InformacionSizer.Add(apuestaPartdaSizer, 0, wx.EXPAND, 0)

        self.apuestaBajaBoton = wx.Button(self, 2, "2")
        self.apuestaBajaBoton.SetMinSize((116, 50))
        self.apuestaBajaBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
        apuestaPartdaSizer.Add(self.apuestaBajaBoton, 1, 0, 0)

        self.apuestaMediaBoton = wx.Button(self, 10, "10")
        self.apuestaMediaBoton.SetMinSize((116, 50))
        self.apuestaMediaBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
        apuestaPartdaSizer.Add(self.apuestaMediaBoton, 1, 0, 0)

        self.apuestaAltaBoton = wx.Button(self, 50, "50")
        self.apuestaAltaBoton.SetMinSize((116, 50))
        self.apuestaAltaBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
        apuestaPartdaSizer.Add(self.apuestaAltaBoton, 1, 0, 0)

        ####################################################################

        self.resultadosPanel = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.resultadosPanel.SetMinSize((300, 242))
        self.resultadosPanel.SetScrollRate(10, 10)
        InformacionSizer.Add(self.resultadosPanel, 1, wx.EXPAND, 0)

        resultadosSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.resultadosPartidaText = wx.StaticText(self.resultadosPanel, wx.ID_ANY, "\nRESULTADOS DE LA PARTIDA:", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.resultadosPartidaText.SetMinSize((350, 422))
        self.resultadosPartidaText.SetBackgroundColour(wx.Colour(253, 249, 196))
        resultadosSizer.Add(self.resultadosPartidaText, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        ####################################################################

        jugarMasSizer = wx.BoxSizer(wx.VERTICAL)
        InformacionSizer.Add(jugarMasSizer, 0, wx.EXPAND, 0)

        self.jugarMasText = wx.StaticText(self, wx.ID_ANY, u"\n¿OTRA PARTIDA?", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.jugarMasText.SetMinSize((350, 50))
        self.jugarMasText.SetBackgroundColour(wx.Colour(253, 249, 196))
        jugarMasSizer.Add(self.jugarMasText, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 1)
        self.jugarMasText.Hide()

        jugarMasBotonesSizer = wx.BoxSizer(wx.HORIZONTAL)
        jugarMasSizer.Add(jugarMasBotonesSizer, 1, wx.EXPAND, 0)

        self.jugarMasSiBoton = wx.Button(self, wx.ID_ANY, "SI")
        self.jugarMasSiBoton.SetMinSize((175, 50))
        self.jugarMasSiBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
        jugarMasBotonesSizer.Add(self.jugarMasSiBoton, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.jugarMasSiBoton.Hide()

        self.jugarMasNoBoton = wx.Button(self, wx.ID_ANY, "NO")
        self.jugarMasNoBoton.SetMinSize((175, 50))
        self.jugarMasNoBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
        jugarMasBotonesSizer.Add(self.jugarMasNoBoton, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.jugarMasNoBoton.Hide()

        ####################################################################

        balancePartidaSizer = wx.BoxSizer(wx.HORIZONTAL)
        InformacionSizer.Add(balancePartidaSizer, 0, wx.EXPAND | wx.TOP, 1)

        balancePartidaText = wx.StaticText(self, wx.ID_ANY, "\nBALANCE DE LA PARTIDA:", style=wx.ALIGN_RIGHT)
        balancePartidaText.SetMinSize((175, 50))
        balancePartidaText.SetBackgroundColour(wx.Colour(253, 249, 196))
        balancePartidaSizer.Add(balancePartidaText, 0, 0, 0)

        self.balancePartidaDato = wx.StaticText(self, wx.ID_ANY, "\n0", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.balancePartidaDato.SetMinSize((175, 50))
        self.balancePartidaDato.SetBackgroundColour(wx.Colour(253, 249, 196))
        balancePartidaSizer.Add(self.balancePartidaDato, 0, 0, 0)

        ####################################################################

        balanceJuegoSizer = wx.BoxSizer(wx.HORIZONTAL)
        InformacionSizer.Add(balanceJuegoSizer, 0, wx.EXPAND | wx.TOP, 1)

        balanceJuegoText = wx.StaticText(self, wx.ID_ANY, "\nBALANCE TOTAL DEL JUEGO:", style=wx.ALIGN_RIGHT)
        balanceJuegoText.SetMinSize((175, 50))
        balanceJuegoText.SetBackgroundColour(wx.Colour(253, 249, 196))
        balanceJuegoSizer.Add(balanceJuegoText, 0, 0, 0)

        self.balanceJuegoDato = wx.StaticText(self, wx.ID_ANY, "\n0", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.balanceJuegoDato.SetMinSize((175, 50))
        self.balanceJuegoDato.SetBackgroundColour(wx.Colour(253, 249, 196))
        balanceJuegoSizer.Add(self.balanceJuegoDato, 0, 0, 0)

        ####################################################################

        self.salirBoton = wx.Button(self, wx.ID_ANY, "SALIR")
        self.salirBoton.SetMinSize((350, 50))
        self.salirBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
        InformacionSizer.Add(self.salirBoton, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        ####################################################################
        ####################################################################
        ####################################################################

        self.PartidaSizer = wx.BoxSizer(wx.VERTICAL)
        AplicacionSizer.Add(self.PartidaSizer, 3, wx.EXPAND | wx.LEFT, 2)

        self.partidaText = wx.StaticText(self, wx.ID_ANY, f"\nPARTIDA #{self.contPartidas}\n", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.partidaText.SetMinSize((1500, 50))
        self.partidaText.SetBackgroundColour(wx.Colour(253, 249, 196))
        self.PartidaSizer.Add(self.partidaText, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 2)

        ####################################################################

        

        ####################################################################
        ####################################################################

        

        self.resultadosPanel.SetSizer(resultadosSizer)

        self.SetSizer(AplicacionSizer)

        self.Layout()

        self.Bind(wx.EVT_CHOICE, self.cambioModo, self.modoPartidaChoice)
        self.Bind(wx.EVT_BUTTON, self.apuestaBaja, self.apuestaBajaBoton)
        self.Bind(wx.EVT_BUTTON, self.apuestaMedia, self.apuestaMediaBoton)
        self.Bind(wx.EVT_BUTTON, self.apuestaAlta, self.apuestaAltaBoton)
        self.Bind(wx.EVT_BUTTON, self.jugarMasSi, self.jugarMasSiBoton)
        self.Bind(wx.EVT_BUTTON, self.jugarMasNo, self.jugarMasNoBoton)
        self.Bind(wx.EVT_BUTTON, self.salir, self.salirBoton)
        
        # end wxGlade

    def cambioModo(self, event):  
        #Cambia el modo de la partida con el evento del objeto wx.Choice
        
        if self.modoPartidaChoice.GetSelection() == 0:
            self.variables.modoPartida = 'J'
        else:
            self.variables.modoPartida = 'A'

        event.Skip()

    def apuestaBaja(self, event):  
        #Asigna a la mano del jugador la apuesta baja al pulsar su respectivo botón

        if self.variables.jugador[0].apuesta == 0:

            self.apuestaMediaBoton.Hide()
            self.apuestaAltaBoton.Hide()

            self.variables.jugador[0].apuesta = self.apuestaBajaBoton.GetId()

            self.repartoInicial()

        event.Skip()

    def apuestaMedia(self, event):  
        #Asigna a la mano del jugador la apuesta media al pulsar su respectivo botón

        if self.variables.jugador[0].apuesta == 0:

            self.apuestaBajaBoton.Hide()
            self.apuestaAltaBoton.Hide()

            self.variables.jugador[0].apuesta = self.apuestaMediaBoton.GetId()

            self.repartoInicial()

        event.Skip()

    def apuestaAlta(self, event):  
        #Asigna a la mano del jugador la apuesta alta al pulsar su respectivo botón

        if self.variables.jugador[0].apuesta == 0:

            self.apuestaMediaBoton.Hide()
            self.apuestaBajaBoton.Hide()

            self.variables.jugador[0].apuesta = self.apuestaAltaBoton.GetId()

            self.repartoInicial()

        event.Skip()

    def jugarMasSi(self, event):  
        #Reinicia la pantalla para poder iniciar de cero una partida nueva al darle a su repectivo botón

        self.contPartidas += 1
        self.partidaText.SetLabelText(f'\nPARTIDA #{self.contPartidas}\n')
        
        self.infoManoCroupier.Hide()
        self.variables.croupier.panel.Destroy()
        
        for i in self.variables.jugador:
            i.botonMano.Hide()
            i.infoMano.Hide()
        self.manosJugadorPanel.Destroy()

        self.manosJugadorText.Hide()
        self.manoCroupierText.Hide()
        
        self.variables.setVariables()
        
        self.apuestaBajaBoton.Show()
        self.apuestaMediaBoton.Show()
        self.apuestaAltaBoton.Show()

        self.resultadosPartidaText.SetLabelText("\nRESULTADOS DE LA PARTIDA:")

        self.jugarMasText.Hide()
        self.jugarMasNoBoton.Hide()
        self.jugarMasSiBoton.Hide()

        self.Layout()

        event.Skip()

    def jugarMasNo(self, event):  
        #Termina el funcionamiento del programa al darle a su respectivo botón

        self.variables.finPartida = True

        self.jugarMasText.Hide()
        self.jugarMasNoBoton.Hide()
        self.jugarMasSiBoton.Hide()

        self.Layout()

        event.Skip()

    def salir(self, event):  
        #Cierra el programa al darle a su respectivo botón

        exit()

    def seleccionarMano(self, event):  
        #Determina cúal ha sido la mano seleccionada para realizar una acción sobre ella al darle a uno de los botones de la mano

        if not self.variables.finPartida:
        
            for i in self.variables.jugador:
                if event.GetEventObject().GetLabelText() == i.nombre:
                    self.variables.manoSeleccionada = i
                    break

            for i in self.variables.jugador:
                if i.estado != 'Cerrada' or i.estado != 'Pasada':
                    i.botonMano.SetBackgroundColour(wx.Colour(255,255,255))

            self.variables.manoSeleccionada.botonMano.SetBackgroundColour(wx.Colour(125,125,125))

            if self.variables.manoSeleccionada.estado != 'Cerrada' and self.variables.manoSeleccionada.estado != 'Pasada':
            
                self.pedirBoton.Show()
                self.doblarBoton.Show()
                self.cerrarBoton.Show()
                
                if len(self.variables.manoSeleccionada.cartas) == 2 and self.variables.manoSeleccionada.cartas[0].valor == self.variables.manoSeleccionada.cartas[1].valor:
                    self.separarBoton.Show()

                self.Layout()
                
        event.Skip()

    def Pedir(self, event):  
        #Añade una carta a la mano seleccionada y acutaliza su información al darle a su respectivo botón

        self.reparte(self.variables.manoSeleccionada)
        self.anadirCarta(self.variables.manoSeleccionada, self.variables.manoSeleccionada.cartas[len(self.variables.manoSeleccionada.cartas)-1])

        self.variables.manoSeleccionada.valorYEstado(self.variables.manoSeleccionada)
        self.variables.manoSeleccionada.infoMano.SetLabelText(f"Valor: {self.variables.manoSeleccionada.valor}\nEstado: {self.variables.manoSeleccionada.estado}\nApuesta: {self.variables.manoSeleccionada.apuesta}")

        self.pedirBoton.Hide()
        self.doblarBoton.Hide()
        self.cerrarBoton.Hide()
        self.separarBoton.Hide()

        self.variables.manoSeleccionada.botonMano.SetBackgroundColour(wx.Colour(255,255,255))
        
        self.comprobaciones('finJugador')

        self.Layout()        

        event.Skip()

    def Doblar(self, event):  
        #Añade una carta a la mano seleccionada y duplica la apuesta de esta al darle a su respectivo botón

        self.reparte(self.variables.manoSeleccionada)
        self.anadirCarta(self.variables.manoSeleccionada, self.variables.manoSeleccionada.cartas[len(self.variables.manoSeleccionada.cartas)-1])
        self.variables.manoSeleccionada.apuesta *= 2

        self.Cerrar(event)

        event.Skip()

    def Cerrar(self, event):  
        #Determina el estado de la mano seleccionada como 'Cerrada' y actualiza su información al darle a su respectivo botón

        self.variables.manoSeleccionada.estado = 'Cerrada'

        self.variables.manoSeleccionada.valorYEstado(self.variables.manoSeleccionada)
        self.variables.manoSeleccionada.infoMano.SetLabelText(f"Valor: {self.variables.manoSeleccionada.valor}\nEstado: {self.variables.manoSeleccionada.estado}\nApuesta: {self.variables.manoSeleccionada.apuesta}")

        self.pedirBoton.Hide()
        self.doblarBoton.Hide()
        self.cerrarBoton.Hide()
        self.separarBoton.Hide()

        self.variables.manoSeleccionada.botonMano.SetBackgroundColour(wx.Colour(255,255,255))

        self.comprobaciones('finJugador')

        self.Layout()        

        event.Skip()

    def Separar(self, event):  
        #Crea una mano nueva, le añade la última carta de la mano seleccionada, les modifica el nombre a ambas, copia su apuesta y actualiza la información de ambas manos

        #Creación de la nueva mano
        aux = Mano()
        aux.cartas.append(self.variables.manoSeleccionada.cartas[len(self.variables.manoSeleccionada.cartas)-1])
        aux.cartasVisuales.append(self.variables.manoSeleccionada.cartasVisuales[len(self.variables.manoSeleccionada.cartasVisuales)-1])
        self.variables.jugador.append(aux)
        self.anadirMano(self.variables.jugador[len(self.variables.jugador)-1])
        self.anadirCarta(self.variables.jugador[len(self.variables.jugador)-1], self.variables.jugador[len(self.variables.jugador)-1].cartas[0])

        del self.variables.manoSeleccionada.cartas[len(self.variables.manoSeleccionada.cartas)-1]
        self.variables.manoSeleccionada.cartasVisuales[len(self.variables.manoSeleccionada.cartasVisuales)-1].Destroy()
        del self.variables.manoSeleccionada.cartasVisuales[len(self.variables.manoSeleccionada.cartasVisuales)-1]

        #Modificación de los nombres        
        self.variables.jugador[len(self.variables.jugador)-1].nombre = self.variables.manoSeleccionada.nombre + 'B'
        self.variables.manoSeleccionada.nombre += 'A'

        #Copia de la apuesta
        self.variables.jugador[len(self.variables.jugador)-1].apuesta = self.variables.manoSeleccionada.apuesta

        #Actualización de la información de las manos
        self.variables.manoSeleccionada.valorYEstado(self.variables.manoSeleccionada)
        self.variables.manoSeleccionada.infoMano.SetLabelText(f"Valor: {self.variables.manoSeleccionada.valor}\nEstado: {self.variables.manoSeleccionada.estado}\nApuesta: {self.variables.manoSeleccionada.apuesta}")
        self.variables.manoSeleccionada.botonMano.SetLabelText(f'{self.variables.manoSeleccionada.nombre}')

        self.variables.jugador[len(self.variables.jugador)-1].valorYEstado(self.variables.jugador[len(self.variables.jugador)-1])
        self.variables.jugador[len(self.variables.jugador)-1].infoMano.SetLabelText(f"Valor: {self.variables.jugador[len(self.variables.jugador)-1].valor}\nEstado: {self.variables.jugador[len(self.variables.jugador)-1].estado}\nApuesta: {self.variables.jugador[len(self.variables.jugador)-1].apuesta}")
        self.variables.jugador[len(self.variables.jugador)-1].botonMano.SetLabelText(f'{self.variables.jugador[len(self.variables.jugador)-1].nombre}')

        self.pedirBoton.Hide()
        self.doblarBoton.Hide()
        self.cerrarBoton.Hide()
        self.separarBoton.Hide()

        self.variables.manoSeleccionada.botonMano.SetBackgroundColour(wx.Colour(255,255,255))
        
        self.comprobaciones('finJugador')

        self.Layout()

        event.Skip()

    def repartoInicial(self):
        #Inicia la partida cuando se elige una apuesta, crea todo lo necesario para poder ver la partida en pantalla

        BlackJack = False

        self.manoCroupierText = wx.StaticText(self, wx.ID_ANY, "MANO DEL CROUPIER")
        self.manoCroupierText.SetMinSize((297, 50))
        self.manoCroupierText.SetForegroundColour(wx.Colour(255, 255, 255))
        self.manoCroupierText.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 1, ""))
        self.PartidaSizer.Add(self.manoCroupierText, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 9)

        self.Layout()
        
        #####

        self.manosCroupierPanel = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.manosCroupierPanel.SetMinSize((1174, 150))
        self.manosCroupierPanel.SetScrollRate(10, 10)
        self.PartidaSizer.Add(self.manosCroupierPanel, 0, wx.EXPAND, 0)
        self.variables.croupier.panel = self.manosCroupierPanel

        manoCroupierSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.variables.croupier.manoSizer = manoCroupierSizer

        #####

        self.infoManoCroupier = wx.StaticText(self.variables.croupier.panel, wx.ID_ANY, "Croupier\nValor: \nEstado: ")
        self.infoManoCroupier.SetMinSize((125, 100))
        self.infoManoCroupier.SetForegroundColour(wx.Colour(255, 255, 255))
        self.infoManoCroupier.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        self.variables.croupier.manoSizer.Add(self.infoManoCroupier, 0, 0, 0)

        #####

        cartasCroupierSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.variables.croupier.manoSizer.Add(cartasCroupierSizer, 1, wx.EXPAND, 0)
        self.variables.croupier.cartasSizer = cartasCroupierSizer

        self.reparte(self.variables.croupier)
        self.anadirCarta(self.variables.croupier, self.variables.croupier.cartas[0])

        self.variables.croupier.valorYEstado(self.variables.croupier)
        self.infoManoCroupier.SetLabelText(f"Croupier\nValor: {self.variables.croupier.valor}\nEstado: {self.variables.croupier.estado}")

        self.variables.croupier.panel.Layout()

        ####################################################################
        ####################################################################

        self.manosJugadorText = wx.StaticText(self, wx.ID_ANY, "MANOS DEL JUGADOR")
        self.manosJugadorText.SetMinSize((306, 50))
        self.manosJugadorText.SetForegroundColour(wx.Colour(255, 255, 255))
        self.manosJugadorText.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 1, ""))
        self.PartidaSizer.Add(self.manosJugadorText, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)

        self.Layout()

        #####

        self.manosJugadorPanel = wx.ScrolledWindow(self, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.manosJugadorPanel.SetScrollRate(10, 10)
        self.PartidaSizer.Add(self.manosJugadorPanel, 1, wx.EXPAND, 0)

        self.manosJugadorSizer = wx.BoxSizer(wx.VERTICAL)

        #####

        self.anadirMano(self.variables.jugador[0])
        self.reparte(self.variables.jugador[0])
        self.anadirCarta(self.variables.jugador[0], self.variables.jugador[0].cartas[0])
        self.reparte(self.variables.jugador[0])
        self.anadirCarta(self.variables.jugador[0], self.variables.jugador[0].cartas[1])

        self.variables.jugador[0].valorYEstado(self.variables.jugador[0])
        self.variables.jugador[0].infoMano.SetLabelText(f"Valor: {self.variables.jugador[0].valor}\nEstado: {self.variables.jugador[0].estado}\nApuesta: {self.variables.jugador[0].apuesta}")

        self.variables.jugador[0].panel.Layout()

        ####################################################################

        if self.variables.jugador[0].valor == 21:
            BlackJack = True
            self.variables.finPartida = True

            self.variables.jugador[0].apuesta = int(self.variables.jugador[0].apuesta * 3/2)
            
            self.resultadosPartidaText.SetLabelText(self.resultadosPartidaText.GetLabelText() + '\n\u256D\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256E\n\u2502 BLACKJACK \u2502\n\u2570\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256F')

            self.comprobaciones('balance')

        if not BlackJack:

            jugadasSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.PartidaSizer.Add(jugadasSizer, 0, wx.EXPAND, 0)

            self.pedirBoton = wx.Button(self, wx.ID_ANY, "PEDIR")
            self.pedirBoton.SetMinSize((204, 50))
            self.pedirBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
            jugadasSizer.Add(self.pedirBoton, 1, wx.ALIGN_CENTER_VERTICAL, 0)
            self.pedirBoton.Hide()

            self.doblarBoton = wx.Button(self, wx.ID_ANY, "DOBLAR")
            self.doblarBoton.SetMinSize((204, 50))
            self.doblarBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
            jugadasSizer.Add(self.doblarBoton, 1, wx.ALIGN_CENTER_VERTICAL, 0)
            self.doblarBoton.Hide()

            self.cerrarBoton = wx.Button(self, wx.ID_ANY, "CERRAR")
            self.cerrarBoton.SetMinSize((204, 50))
            self.cerrarBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
            jugadasSizer.Add(self.cerrarBoton, 1, wx.ALIGN_CENTER_VERTICAL, 0)
            self.cerrarBoton.Hide()

            self.separarBoton = wx.Button(self, wx.ID_ANY, "SEPARAR")
            self.separarBoton.SetMinSize((205, 50))
            self.separarBoton.SetBackgroundColour(wx.Colour(255, 255, 255))
            jugadasSizer.Add(self.separarBoton, 1, wx.ALIGN_CENTER_VERTICAL, 0)
            self.separarBoton.Hide()
            
            self.Bind(wx.EVT_BUTTON, self.Pedir, self.pedirBoton)
            self.Bind(wx.EVT_BUTTON, self.Doblar, self.doblarBoton)
            self.Bind(wx.EVT_BUTTON, self.Cerrar, self.cerrarBoton)
            self.Bind(wx.EVT_BUTTON, self.Separar, self.separarBoton)

        self.manosJugadorPanel.SetSizer(self.manosJugadorSizer)

        self.manosCroupierPanel.SetSizer(manoCroupierSizer)

        self.Layout()

    def anadirMano(self, mano):
        #Añade una mano a la interfaz gráfica con los datos de la mano que se le envía

        mano.panel = self.manosJugadorPanel

        mano.manoSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.manosJugadorSizer.Add(mano.manoSizer, 0, wx.BOTTOM | wx.EXPAND, 20)

        mano.botonMano = wx.Button(mano.panel, wx.ID_ANY, f"{mano.nombre}")
        mano.botonMano.SetMinSize((75, 75))
        mano.manoSizer.Add(mano.botonMano, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)

        mano.infoMano = wx.StaticText(mano.panel, wx.ID_ANY, '')
        mano.infoMano.SetMinSize((125, 75))
        mano.infoMano.SetForegroundColour(wx.Colour(255, 255, 255))
        mano.infoMano.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "Segoe UI"))
        mano.manoSizer.Add(mano.infoMano, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        
        mano.cartasSizer = wx.BoxSizer(wx.HORIZONTAL)
        mano.manoSizer.Add(mano.cartasSizer, 1, wx.EXPAND, 0)

        self.Bind(wx.EVT_BUTTON, self.seleccionarMano, mano.botonMano)

    def anadirCarta(self, mano, carta):
        #Añade una carta visual a la interfaz gráfica en la mano enviada con los datos de la carta enviada

        mano.cartasVisuales.append(wx.StaticBitmap(mano.panel, wx.ID_ANY, wx.Bitmap(f'cartas\\{str(carta.ind)}.png')))
        mano.cartasSizer.Add(mano.cartasVisuales[len(mano.cartasVisuales)-1], 0, wx.LEFT | wx.RIGHT, 10)

    def reparte(self, mano):
        #Reparte una carta del mazo y la añade a la mano que se le envía

        carta = self.mazo.reparte()
        carta.representaCarta(carta)

        mano.cartas.append(carta)

    def comprobaciones(self, variable):
        #Realiza diferentes acciones en función de la variable que se le envíe

        if variable == 'finJugador':
            #Comprueba si todas las manos del jugador están cerradas o pasadas
        
            contPasadas = 0
            contCerradas = 0

            for i in self.variables.jugador:

                if i.estado == 'Pasada':
                    contPasadas += 1
                elif i.estado == 'Cerrada':
                    contCerradas += 1
                
            if contPasadas == len(self.variables.jugador):
                self.variables.turnoCroupier = False
                self.variables.finPartida = True
                
            if contCerradas + contPasadas == len(self.variables.jugador) and self.variables.turnoCroupier:
                self.turnoCroupier()

            elif not self.variables.turnoCroupier:
                variable = 'balance'

        if variable == 'balance':
            #Llama al método que realiza el balance de la partida

            self.balance()

    def balance(self):
        #Realiza el balance de la partida y lo muestra en pantalla

        balance = 0
        signoBalance = ''

        for i in self.variables.jugador:

            signo = '' #Signo visible en los resultados
            iguales = False #Para saber si la mano del jugador y del croupier tienen el mismo valor o ambas están pasadas

            if i.valor > self.variables.croupier.valor and i.estado != 'Pasada' and self.variables.croupier.estado != 'Pasada':
                
                signo = '+'
                i.botonMano.SetBackgroundColour(wx.Colour(150,255,150))

                self.balancePartida += i.apuesta
                self.balanceTotal += i.apuesta
                balance += i.apuesta

            elif i.valor < self.variables.croupier.valor and i.estado != 'Pasada' and self.variables.croupier.estado != 'Pasada':
                
                signo = '-'
                i.botonMano.SetBackgroundColour(wx.Colour(255,150,150))

                self.balancePartida -= i.apuesta
                self.balanceTotal -= i.apuesta
                balance -= i.apuesta

            elif i.estado != 'Pasada' and self.variables.croupier.estado == 'Pasada':
                
                signo = '+'
                i.botonMano.SetBackgroundColour(wx.Colour(150,255,150))

                self.balancePartida += i.apuesta
                self.balanceTotal += i.apuesta
                balance += i.apuesta

            elif i.estado == 'Pasada' and self.variables.croupier.estado != 'Pasada':
                
                signo = '-'
                i.botonMano.SetBackgroundColour(wx.Colour(255,150,150))

                self.balancePartida -= i.apuesta
                self.balanceTotal -= i.apuesta
                balance -= i.apuesta

            elif i.estado == 'Pasada' and self.variables.croupier.estado == 'Pasada' or i.valor == self.variables.croupier.valor:
                
                iguales = True
                i.botonMano.SetBackgroundColour(wx.Colour(150,150,255))
                
                self.resultadosPartidaText.SetLabelText(self.resultadosPartidaText.GetLabelText() + f'\nCroupier: {self.variables.croupier.valor} // {i.nombre}: {i.valor} ===> +0')

            if not iguales:
                self.resultadosPartidaText.SetLabelText(self.resultadosPartidaText.GetLabelText() + f'\nCroupier: {self.variables.croupier.valor} // {i.nombre}: {i.valor} ===> {signo}{i.apuesta}')

        if balance >= 0:
            signoBalance = '+'
        else:
            signoBalance = '-'
        
        self.resultadosPartidaText.SetLabelText(self.resultadosPartidaText.GetLabelText() + f'\nTotal de la partida: {signoBalance}{int(balance)}')

        self.balancePartidaDato.SetLabelText('\n' + str(self.balancePartida))
        self.balanceJuegoDato.SetLabelText('\n' + str(self.balanceTotal))

        self.jugarMasText.Show()
        self.jugarMasSiBoton.Show()
        self.jugarMasNoBoton.Show()

        self.Layout()

    def turnoCroupier(self):
        #Realiza el turno del Croupier

        while self.variables.croupier.valor <= 17:

            self.reparte(self.variables.croupier)
            self.anadirCarta(self.variables.croupier, self.variables.croupier.cartas[len(self.variables.croupier.cartas)-1])

            self.variables.croupier.valorYEstado(self.variables.croupier)
            self.infoManoCroupier.SetLabelText(f"Croupier\nValor: {self.variables.croupier.valor}\nEstado: {self.variables.croupier.estado}")

            self.Layout()

        self.variables.finPartida = True

        self.comprobaciones('balance')

# end of class BlackJackInterfaz

class MyApp(wx.App):
    def OnInit(self):
        self.BJWindow = BlackJackInterfaz(None, wx.ID_ANY, "")
        self.SetTopWindow(self.BJWindow)
        self.BJWindow.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()