import pygame
import numpy as np
import math

# Inicializar pygame
pygame.init()

# Definir o tamanho da tela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Formas Girando 3D")

# Definir cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Função para gerar vértices e arestas de um cubo
def create_cube():
    vertices = np.array([
        [-1, -1, -1],
        [-1, -1,  1],
        [-1,  1, -1],
        [-1,  1,  1],
        [ 1, -1, -1],
        [ 1, -1,  1],
        [ 1,  1, -1],
        [ 1,  1,  1]
    ])
    edges = [(0, 1), (1, 3), (3, 2), (2, 0),  # Conexões das faces frontais
             (4, 5), (5, 7), (7, 6), (6, 4),  # Conexões das faces traseiras
             (0, 4), (1, 5), (2, 6), (3, 7)]  # Conexões entre a face frontal e traseira
    return vertices, edges

# Função para gerar vértices e arestas de uma pirâmide
def create_pyramid():
    vertices = np.array([
        [-1, -1, -1],  # Base
        [ 1, -1, -1],
        [ 1,  1, -1],
        [-1,  1, -1],
        [ 0,  0,  1]   # Vértice do topo
    ])
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),  # Conexões da base
             (0, 4), (1, 4), (2, 4), (3, 4)]  # Conexões da base ao topo
    return vertices, edges

# Definir a matriz de projeção (pinhole camera)
projection_matrix = np.array([
    [1, 0, 0],
    [0, 1, 0]
])

# Função de rotação em torno dos eixos X, Y, Z
def rotate_x(point, angle):
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])
    return np.dot(rotation_matrix, point)

def rotate_y(point, angle):
    rotation_matrix = np.array([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])
    return np.dot(rotation_matrix, point)

def rotate_z(point, angle):
    rotation_matrix = np.array([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])
    return np.dot(rotation_matrix, point)

# Projeção 3D para 2D usando a matriz de projeção
def project(point):
    projected_point = np.dot(projection_matrix, point)
    x = int(projected_point[0] * 200 + width // 2)  # Escalar e centralizar
    y = int(projected_point[1] * 200 + height // 2)
    return (x, y)

# Variáveis para controlar a rotação
angle_x = angle_y = angle_z = 0
current_shape = 1  # 1 = cubo, 2 = pirâmide

# Função para alternar entre formas com base nas teclas pressionadas
def handle_shape_change(keys):
    global current_shape
    if keys[pygame.K_1]:
        current_shape = 1  # Cubo
    if keys[pygame.K_2]:
        current_shape = 2  # Pirâmide

# Função para processar a rotação com base nas teclas pressionadas
def handle_rotation(keys):
    global angle_x, angle_y, angle_z
    if keys[pygame.K_i]:  # Rotacionar em torno do eixo X (I)
        angle_x += 0.05
    if keys[pygame.K_k]:  # Rotacionar em torno do eixo X (K)
        angle_x -= 0.05
    if keys[pygame.K_j]:  # Rotacionar em torno do eixo Y (J)
        angle_y += 0.05
    if keys[pygame.K_l]:  # Rotacionar em torno do eixo Y (L)
        angle_y -= 0.05
    if keys[pygame.K_u]:  # Rotacionar em torno do eixo Z (U)
        angle_z += 0.05
    if keys[pygame.K_o]:  # Rotacionar em torno do eixo Z (O)
        angle_z -= 0.05

# Loop principal
running = True
while running:
    screen.fill(BLACK)

    # Verificar eventos (fechar janela)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capturar o estado do teclado
    keys = pygame.key.get_pressed()
    
    # Controle de forma
    handle_shape_change(keys)
    
    # Controle da rotação
    handle_rotation(keys)

    # Definir a forma atual com base na tecla pressionada
    if current_shape == 1:
        vertices, edges = create_cube()
    elif current_shape == 2:
        vertices, edges = create_pyramid()

    # Rotacionar e projetar os vértices da forma
    transformed_vertices = []
    for vertex in vertices:
        rotated_vertex = rotate_x(vertex, angle_x)
        rotated_vertex = rotate_y(rotated_vertex, angle_y)
        rotated_vertex = rotate_z(rotated_vertex, angle_z)
        
        # Projeção 3D para 2D
        projected_vertex = project(rotated_vertex)
        transformed_vertices.append(projected_vertex)

    # Desenhar as arestas da forma
    for edge in edges:
        point1 = transformed_vertices[edge[0]]
        point2 = transformed_vertices[edge[1]]
        pygame.draw.line(screen, WHITE, point1, point2, 2)

    # Atualizar a tela
    pygame.display.flip()
    pygame.time.delay(10)

# Fechar pygame
pygame.quit()
