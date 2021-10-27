import unittest
from generala import (
    Dados,
    Generala,
    TablaPuntosError,
    TurnoError,
    calcular_repetidos,
    calcular_puntos,
    Turno,
    TablaPuntos,
)


class TurnoTest(unittest.TestCase):

    def test_tirada_1(self):
        turno = Turno()
        self.assertEqual(turno.numero_lanzamiento, 1)

    def test_tirada_2(self):
        turno = Turno()
        turno.siguiente_turno()
        self.assertEqual(turno.numero_lanzamiento, 2)

    def test_tirada_3(self):
        turno = Turno()
        turno.siguiente_turno()
        turno.siguiente_turno()
        self.assertEqual(turno.numero_lanzamiento, 3)

    def test_tirada_4(self):
        turno = Turno()
        turno.siguiente_turno()
        turno.siguiente_turno()
        with self.assertRaises(TurnoError):
            turno.siguiente_turno()  # No puede haber un 4to turno
        self.assertEqual(turno.numero_lanzamiento, 3)  # Verifico que el numero de lanzamiento haya quedado en 3

    def test_cant_dados(self):
        turno = Turno()
        self.assertEqual(turno.dados_lanzados.cantidad, 5)
        self.assertEqual(len(turno.dados_finales), 5)

    def test_can_dados_turno2_1dado(self):
        turno = Turno()
        turno.guardar_dados([3])  # Los que NO vamos a tirar de nuevos (Guardamos uno)
        self.assertEqual(turno.dados_seguir.cantidad, 1)
        self.assertEqual(turno.dados_lanzados.cantidad, 4)

    def test_can_dados_turno2_2dado(self):
        turno = Turno()
        turno.guardar_dados([3, 1])  # Los que NO vamos a tirar de nuevos (Guardamos uno)
        self.assertEqual(turno.dados_seguir.cantidad, 2)
        self.assertEqual(turno.dados_lanzados.cantidad, 3)

    def test_can_dados_turno2_4dado(self):
        turno = Turno()
        turno.guardar_dados([0, 1, 2, 3])  # Los que NO vamos a tirar de nuevos (Guardamos uno)
        self.assertEqual(turno.dados_seguir.cantidad, 4)
        self.assertEqual(turno.dados_lanzados.cantidad, 1)


class TablaPuntosTest(unittest.TestCase):
    def test_anotar_doble(self):
        tabla = TablaPuntos(2)
        jugador = 0
        jugada = 'poker'
        numero_lanzamiento = 1
        dados = [1, 1, 1, 1, 1]
        tabla.anotar(jugador, jugada, numero_lanzamiento, dados)
        self.assertEqual(tabla._tabla[0]['poker'], 45)
        dados = [2, 2, 1, 1, 1]
        with self.assertRaises(TablaPuntosError):
            tabla.anotar(jugador, jugada, numero_lanzamiento, dados)
        self.assertEqual(tabla._tabla[0]['poker'], 45)


class CalcularPuntosTest(unittest.TestCase):
    def test_calcular_puntos_1_0_puntos(self):
        dados = [2, 2, 3, 4, 5]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "1")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_1_1_punto(self):
        dados = [2, 1, 3, 4, 5]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "1")
        self.assertEqual(puntos, 1)

    def test_calcular_puntos_1_2_puntos(self):
        dados = [2, 1, 1, 4, 5]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "1")
        self.assertEqual(puntos, 2)

    def test_calcular_puntos_1_5_puntos(self):
        dados = [1, 1, 1, 1, 1]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "1")
        self.assertEqual(puntos, 5)

    def test_calcular_puntos_2_2_puntos(self):
        dados = [2, 1, 3, 4, 5]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "2")
        self.assertEqual(puntos, 2)

    def test_calcular_puntos_2_10_puntos(self):
        dados = [2, 2, 2, 2, 2]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "2")
        self.assertEqual(puntos, 10)

    def test_calcular_puntos_6_30_puntos(self):
        dados = [6, 6, 6, 6, 6]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "6")
        self.assertEqual(puntos, 30)

    def test_calcular_puntos_generala_puntos_50(self):
        dados = [6, 6, 6, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "generala")
        self.assertEqual(puntos, 50)

    def test_calcular_puntos_generala_puntos_0(self):
        dados = [6, 6, 4, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "generala")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_poker_puntos_40_por_5(self):
        dados = [6, 6, 6, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "poker")
        self.assertEqual(puntos, 40)

    def test_calcular_puntos_poker_puntos_40_por_4(self):
        dados = [6, 6, 4, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "poker")
        self.assertEqual(puntos, 40)

    def test_calcular_puntos_poker_puntos_45_servido(self):
        dados = [6, 6, 4, 6, 6]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "poker")
        self.assertEqual(puntos, 45)

    def test_calcular_puntos_poker_puntos_0(self):
        dados = [6, 3, 4, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "poker")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_full_puntos_30(self):
        dados = [3, 3, 6, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "full")
        self.assertEqual(puntos, 30)

    def test_calcular_puntos_full_puntos_0_2(self):
        dados = [6, 6, 6, 6, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "full")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_full_puntos_35(self):
        dados = [3, 6, 6, 3, 6]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "full")
        self.assertEqual(puntos, 35)

    def test_calcular_puntos_full_puntos_0(self):
        dados = [3, 3, 3, 2, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "full")
        self.assertEqual(puntos, 0)
    
    def test_calcular_puntos_generala_doble_sin_generala(self):
        dados = [3,3,3,3,3]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "generala_doble")
        self.assertEqual(puntos, 0)

    def test_calcular_puntos_generala_doble_con_generala(self):
        juego = Generala(1)
        dados = [3,3,3,3,3]
        puntos = calcular_puntos(2, dados, "generala")
        juego.tabla_puntos.anotar(0,'generala',2,dados)
        self.assertEqual(juego.tabla_puntos._tabla[0]['generala'], 50)
        dados = [1,1,1,1,1]
        juego.tabla_puntos.anotar(0,'generala_doble',2,dados)
        self.assertEqual(juego.tabla_puntos._tabla[0]['generala_doble'], 100)

    def test_calcular_puntos_generala_doble_con_generala2(self):
        juego = Generala(1)
        dados = [3,3,3,3,3]
        puntos = calcular_puntos(2, dados, "generala")
        juego.tabla_puntos.anotar(0,'generala',2,dados)
        self.assertEqual(juego.tabla_puntos._tabla[0]['generala'], 50)
        dados = [3,3,3,3,3]
        juego.tabla_puntos.anotar(0,'generala_doble',2,dados)
        self.assertEqual(juego.tabla_puntos._tabla[0]['generala_doble'], 100)

    def test_calcular_puntos_generala_doble_con_generala_tachada(self):
        juego = Generala(1)
        dados = [3,2,2,3,4]
        puntos = calcular_puntos(2, dados, "generala")
        juego.tabla_puntos.anotar(0,'generala',2,dados)
        self.assertEqual(juego.tabla_puntos._tabla[0]['generala'], 0)
        dados = [1,1,1,1,1]
        juego.tabla_puntos.anotar(0,'generala_doble',2,dados)
        self.assertEqual(juego.tabla_puntos._tabla[0]['generala_doble'], 0)


    def test_calcular_dados_iguales_dobles(self):
        dados = [1, 2, 2, 3, 6]
        repetidos = calcular_repetidos(dados)
        self.assertEqual(
            repetidos, [
                1,  # 1
                2,  # 2
                1,  # 3
                0,  # 4
                0,  # 5
                1,  # 6
            ]
        )

    def test_calcular_dados_iguales_trios(self):
        dados = [1, 3, 2, 3, 3]
        repetidos = calcular_repetidos(dados)
        self.assertEqual(
            repetidos, [
                1,  # 1
                1,  # 2
                3,  # 3
                0,  # 4
                0,  # 5
                0,  # 6
            ]
        )

    def test_calcular_no_escalera(self):
        dados = [1, 2, 5, 4, 5]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "escalera")
        self.assertEqual(puntos, 0)

    def test_calcular_escalera_menor(self):
        dados = [4, 1, 2, 3, 5]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "escalera")
        self.assertEqual(puntos, 20)

    def test_calcular_escalera_mayor(self):
        dados = [2, 3, 4, 5, 6]
        numero_lanzamiento = 2
        puntos = calcular_puntos(numero_lanzamiento, dados, "escalera")
        self.assertEqual(puntos, 20)

    def test_calcular_escalera_mayor_servida(self):
        dados = [2, 3, 4, 5, 6]
        numero_lanzamiento = 1
        puntos = calcular_puntos(numero_lanzamiento, dados, "escalera")
        self.assertEqual(puntos, 25)

    def test_victoria(self):
        juego_terminado = Generala(2,1)
        self.assertTrue(juego_terminado.tabla_puntos.estado_tabla)

    def test_no_victoria(self):
        juego_terminado = Generala(2)
        self.assertFalse(juego_terminado.tabla_puntos.estado_tabla)

    def test_puntajes(self):
        tabla_llena = TablaPuntos(2)
        tabla_llena._tabla = [
            {
                '1': 1,
                '2': 2,
                '3':3,
                '4': 4,
                '5': 5,
                '6': 6,
                'escalera': 20,
                'full': 30,
                'poker': 40,
                'generala': 50,
                'generala_doble': 0,
            },
            {
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
                '6': 0,
                'escalera': 25,
                'full': 35,
                'poker': 45,
                'generala': 50,
                'generala_doble': 0,
            }]
        
        self.assertEqual(tabla_llena.puntajes, {0: 161, 1: 155})


    def test_puntajes_con_None(self):
        tabla_llena = TablaPuntos(2)
        tabla_llena._tabla = [
            {
                '1': 1,
                '2': 2,
                '3':3,
                '4': None,
                '5': 5,
                '6': 6,
                'escalera': None,
                'full': 30,
                'poker': 40,
                'generala': 50,
                'generala_doble': None,
            },
            {
                '1': 0,
                '2': None,
                '3': None,
                '4': 0,
                '5': 0,
                '6': 0,
                'escalera': 25,
                'full': 35,
                'poker': 45,
                'generala': 50,
                'generala_doble': None,
            }]
        
        self.assertEqual(tabla_llena.puntajes, {0: 137, 1: 155} )


    def test_puntajes_vacios(self):
        tabla_llena = TablaPuntos(2)
        tabla_llena._tabla = [
            {
                '1': None,
                '2': None,
                '3':None,
                '4': None,
                '5': None,
                '6': None,
                'escalera': None,
                'full': None,
                'poker': None,
                'generala': None,
                'generala_doble': None,
            },
            {
                '1': 0,
                '2': None,
                '3': None,
                '4': 0,
                '5': 0,
                '6': 0,
                'escalera': 25,
                'full': 35,
                'poker': 45,
                'generala': 50,
                'generala_doble': None,
            }]
        
        self.assertEqual(tabla_llena.puntajes, {0: 0, 1: 155} )


if __name__ == '__main__':
    unittest.main()