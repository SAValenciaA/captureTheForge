import random
import time
from collections import deque

class MapaEstelar:
    def __init__(self, dificultad):
        self.planetas_disponibles = [
            "Mercury", "Venus", "Earth", "Mars", "Jupiter", 
            "Saturn", "Uranus", "Neptune", "Pluto", "Sun"
        ]
        self.num_planetas = self._definir_cantidad_planetas(dificultad)
        self.planetas_juego = self.planetas_disponibles[:self.num_planetas]
        self.conexiones = {planeta: [] for planeta in self.planetas_juego}
        self._generar_conexiones()

    def _definir_cantidad_planetas(self, dificultad):
        if dificultad == 'easy': return 4
        if dificultad == 'medium': return 7
        if dificultad == 'hard': return 10
        return 4

    def _generar_conexiones(self):
        for planeta in self.planetas_juego:
            posibles_destinos = [p for p in self.planetas_juego if p != planeta]
            num_conexiones = random.randint(1, min(3, len(posibles_destinos)))
            destinos = random.sample(posibles_destinos, num_conexiones)
            self.conexiones[planeta].extend(destinos)

    def mostrar_mapa(self):
        print("\n--- CONTECTION OF THE PLANETARY NETWORK ---")
        for origen, destinos in self.conexiones.items():
            rutas = ", ".join(destinos)
            print(f"[{origen}] can go to: -> {rutas}")
        print("------------------------------------------------")

    def obtener_camino_mas_corto(self, inicio, fin):
        cola = deque([[inicio]])
        visitados = set([inicio])

        while cola:
            camino = cola.popleft()
            nodo_actual = camino[-1]

            if nodo_actual == fin:
                return camino

            for vecino in self.conexiones.get(nodo_actual, []):
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = list(camino)
                    nuevo_camino.append(vecino)
                    cola.append(nuevo_camino)
        return None

    def generar_opciones(self, inicio, fin, camino_correcto):
        opciones = []
        opciones.append(camino_correcto)
        intentos = 0
        while len(opciones) < 4 and intentos < 50:
            ruta_falsa = [inicio]
            largo_ruta = random.randint(2, len(camino_correcto) + 2)
            nodo_actual = inicio
            ruta_invalida = False
            
            for _ in range(largo_ruta - 1):
                if random.random() > 0.5:
                    vecinos = self.conexiones.get(nodo_actual, [])
                    if vecinos:
                        siguiente = random.choice(vecinos)
                    else:
                        siguiente = random.choice(self.planetas_juego) 
                        ruta_invalida = True
                else:
                    siguiente = random.choice(self.planetas_juego) 

                ruta_falsa.append(siguiente)
                nodo_actual = siguiente
                
                if nodo_actual == fin:
                    break
            

            if ruta_falsa[-1] != fin:
                ruta_falsa.append(fin)


            if ruta_falsa != camino_correcto and ruta_falsa not in opciones:
                opciones.append(ruta_falsa)
            
            intentos += 1

        while len(opciones) < 4:
            ruta_relleno = [inicio, random.choice(self.planetas_juego), fin]
            if ruta_relleno not in opciones:
                opciones.append(ruta_relleno)

        random.shuffle(opciones)
        return opciones

class Juego:
    def __init__(self):
        self.puntuacion = 0
        self.rondas_totales = 4
        self.tiempo_limite = 30 
        self.puntos_por_ronda = 100

    def mostrar_menu(self):
        while True:
            print("\n========================================")
            print("               Space Trip               ")
            print("========================================")
            print("1. Start Game")
            print("2. Game rules")
            print("3. Exit")
            
            opcion = input("\nSelecciona una opción: ").strip()

            if opcion == "1":
                self.configurar_partida()
            elif opcion == "2":
                self.mostrar_reglas()
            elif opcion == "3":
                print("See you, space cowboy!")
                break
            else:
                print("No valid option.")

    def mostrar_reglas(self):
        print("\n--- Rules ---")
        print(f"* You have {self.rondas_totales} rounds to collect points.")
        print(f"* You have to fint the SHORTEST route between tho planets.")
        print(f"* You have {self.tiempo_limite} seconds per question.")
        print("* You'll win 100 points per correct answer.")
        print("* Concetions are only in one way (Unidirectional).")
        input("Press enter to go back to menu...")

    def configurar_partida(self):
        print("\nSelect Dificulty:")
        print("1. Easy (4 Planets)")
        print("2. Medium (7 Planets)")
        print("3. Hard (10 Planets)")
        
        seleccion = input("Option: ").strip()
        dificultad = 'easy'
        if seleccion == '2': dificultad = 'medium'
        if seleccion == '3': dificultad = 'hard'
        
        self.iniciar_juego(dificultad)

    def iniciar_juego(self, dificultad):
        self.puntuacion = 0
        mapa = MapaEstelar(dificultad)
        mapa.mostrar_mapa()
        input("\nAnalize the map. Press enter to start your mission...")

        for ronda in range(1, self.rondas_totales + 1):
            exito = self.jugar_ronda(ronda, mapa)
            if exito:
                self.puntuacion += self.puntos_por_ronda

        print("\n========================================")
        print(f"🏁 END OF THE ROUND")
        print(f"🏆 FINAL SCORE: {self.puntuacion} Points")
        print("========================================")
        input("Press enter to go back to menu...")

        if self.puntuacion == 400 and dificultad == 'hard':
            print("flag{dijkstra_was_a_boss}")

    def jugar_ronda(self, n_ronda, mapa):
        inicio, fin = None, None
        camino_correcto = None
        
        while camino_correcto is None:
            inicio = random.choice(mapa.planetas_juego)
            fin = random.choice(mapa.planetas_juego)
            if inicio != fin:
                camino_correcto = mapa.obtener_camino_mas_corto(inicio, fin)

        opciones = mapa.generar_opciones(inicio, fin, camino_correcto)
        letras = ['a', 'b', 'c', 'd']
        
        print(f"\n--- ROUND {n_ronda}/{self.rondas_totales} ---")
        print(f"🎯 Mission: Find the shortest way from [{inicio}] to [{fin}]")
        print(f"⏳ You have {self.tiempo_limite} seconds.")

        diccionario_opciones = {}
        for i, opcion_ruta in enumerate(opciones):
            ruta_texto = " -> ".join(opcion_ruta)
            print(f"{letras[i]}) {ruta_texto}")
            diccionario_opciones[letras[i]] = opcion_ruta

        inicio_tiempo = time.time()
        respuesta = input("\nYour answer (a/b/c/d): ").lower().strip()
        fin_tiempo = time.time()
        
        tiempo_transcurrido = fin_tiempo - inicio_tiempo

        if tiempo_transcurrido > self.tiempo_limite:
            print(f"❌ There's no more time! It took you {int(tiempo_transcurrido)}s.")
            print(f"The correct way was: {' -> '.join(camino_correcto)}")
            return False

        if respuesta in diccionario_opciones:
            ruta_seleccionada = diccionario_opciones[respuesta]
            if ruta_seleccionada == camino_correcto:
                print("✅ Correct! succesful find.")
                print(f"The correct way was: {' -> '.join(camino_correcto)}")
                return True
            else:
                print("❌ Wrong answer.")
                print(f"The correct way was: {' -> '.join(camino_correcto)}")
                return False
        else:
            print("❌ Invalid option.")
            print(f"The correct way was: {' -> '.join(camino_correcto)}")
            return False

if __name__ == "__main__":
    juego = Juego()
    juego.mostrar_menu()
