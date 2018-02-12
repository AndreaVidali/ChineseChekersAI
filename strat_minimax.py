from engine_2 import *
import copy


player1_set, player2_set, player3_set, player4_set, player5_set, player6_set = build_sets()
player1_obj, player2_obj, player3_obj, player4_obj, player5_obj, player6_obj = build_obj_sets()
player1_inv_homes, player2_inv_homes, player3_inv_homes, player4_inv_homes, player5_inv_homes, player6_inv_homes = \
    build_invalid_homes_sets(player1_set, player2_set, player3_set, player4_set, player5_set, player6_set, player1_obj,
                             player2_obj, player3_obj, player4_obj, player5_obj, player6_obj)


def minimax(board, depth, player, first_player, player1_set, player2_set, player3_set, player4_set, player5_set, player6_set):

    board_copy = board[:][:]

    if depth == 0:
        prev_player = player - 1
        if prev_player == 0:
            prev_player = 6
        board_score = calculate_board_score(board_copy, prev_player, player1_set, player2_set, player3_set, player4_set, player5_set, player6_set)
        return board_score, None
    
    set_pieces = assign_set(player, player1_set, player2_set, player3_set, player4_set, player5_set, player6_set)
    # set_pieces = find_player_pieces(board, player)

    obj_set = assign_obj_set(player, player1_obj, player2_obj, player3_obj, player4_obj,
                             player5_obj, player6_obj)

    inv_homes_set = assign_invalid_homes_set(player, player1_inv_homes, player2_inv_homes, player3_inv_homes,
                                             player4_inv_homes, player5_inv_homes, player6_inv_homes)

    valid_moves = find_all_legal_moves(board_copy, set_pieces, obj_set, inv_homes_set)

    scores = []
    moves = []

    for move in valid_moves:

        # board_copy = board_copy[:][:]
        # print('--- player', player, "set:", set_pieces)
        # print('- player', player, "- move:", move)

        [start_x, start_y] = move[0]
        [end_x, end_y] = move[1]
        if board_copy[start_x][start_y] != player:
            print("---------------------- board start non ce il player -prima ---", move[0], board_copy[start_x][start_y])
        if board_copy[end_x][end_y] != 0:
            print("---------------------- board end non e vuota -prima ---", move[1], board_copy[end_x][end_y])

        board_copy_again = copy.copy(board_copy)
        new_board, new_set_pieces = do_move(board_copy_again, move, set_pieces)

        [start_x, start_y] = move[0]
        [end_x, end_y] = move[1]
        if board_copy[start_x][start_y] != player:
            print("---------------------- board start non ce il player -dopo ---", move[0], board_copy[start_x][start_y])
        if board_copy[end_x][end_y] != 0:
            print("---------------------- board end non e vuota -dopo ---", move[1], board_copy[end_x][end_y])
        if new_board[start_x][start_y] != 0:
            print("---------------------- nuova board start non vuoto ---", move[0], new_board[start_x][start_y])
        if new_board[end_x][end_y] != player:
            print("---------------------- nuova board end non ce il player ---", move[1], new_board[end_x][end_y])

        player1_set, player2_set, player3_set, player4_set, player5_set, player6_set = \
            update_player_set(new_set_pieces, player, player1_set, player2_set, player3_set, player4_set,
                              player5_set, player6_set)

        next_player = player + 1
        if next_player == 7:
            next_player = 1

        score, something = minimax(new_board, depth - 1, next_player, first_player, player1_set, player2_set, player3_set, player4_set, player5_set, player6_set)
        scores.append(score)
        moves.append(move)
        print('- player', player, 'depth', depth, '- move', move, 'score', score)
        print('---- scores:', scores)
        print('---- moves:', moves)

    if player == first_player:
        max_score_index = scores.index(max(scores))
        best_move = moves[max_score_index]
        print('- player', player, '- best move', best_move, '. score', max(scores), '. at index', max_score_index)
        return scores[max_score_index], best_move

    else:
        min_score_index = scores.index(min(scores))
        worst_opponent_move = moves[min_score_index]
        print('- player', player, '- worst opponent move', worst_opponent_move, '. score', min(scores), '. at index', min_score_index)
        return scores[min_score_index], worst_opponent_move


def calculate_board_score(board, player_turn, p1_pieces, p2_pieces, p3_pieces, p4_pieces, p5_pieces, p6_pieces):

    # p1_pieces = find_player_pieces(board, 1)
    # p2_pieces = find_player_pieces(board, 2)
    # p3_pieces = find_player_pieces(board, 3)
    # p4_pieces = find_player_pieces(board, 4)
    # p5_pieces = find_player_pieces(board, 5)
    # p6_pieces = find_player_pieces(board, 6)

    # print("--- player:", 1, "set:", p1_pieces)
    # print("--- player:", 2, "set:", p2_pieces)
    # print("--- player:", 3, "set:", p3_pieces)
    # print("--- player:", 4, "set:", p4_pieces)
    # print("--- player:", 5, "set:", p5_pieces)
    # print("--- player:", 6, "set:", p6_pieces)

    p1_avg_distance = find_avg_distance(p1_pieces, [16, 12])
    print("-- avg distance p1", p1_avg_distance)
    p2_avg_distance = find_avg_distance(p2_pieces, [12, 0])
    print("-- avg distance p2", p2_avg_distance)
    p3_avg_distance = find_avg_distance(p3_pieces, [4, 0])
    print("-- avg distance p3", p3_avg_distance)
    p4_avg_distance = find_avg_distance(p4_pieces, [0, 12])
    print("-- avg distance p4", p4_avg_distance)
    p5_avg_distance = find_avg_distance(p5_pieces, [4, 24])
    print("-- avg distance p5", p5_avg_distance)
    p6_avg_distance = find_avg_distance(p6_pieces, [12, 24])
    print("-- avg distance p6", p6_avg_distance)

    score = calculate_score(player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance, p4_avg_distance,
                            p5_avg_distance, p6_avg_distance)

    return score


def find_player_pieces(board, player):

    p_pieces = []
    p_coords = np.where(board == player)
    # print("--- player:", player, "set vago:", p_coords[0], p_coords[1])
    for i in range(0, 10):
        x = p_coords[0][i]
        y = p_coords[1][i]
        p_pieces.append([x, y])

    return p_pieces


def find_avg_distance(p_pieces, obj):

    total_distance = 0
    [obj_x, obj_y] = obj

    for piece in p_pieces:

        [x, y] = piece

        square_y = (y * 14.43) / 25
        square_obj_y = (obj_y * 14.43) / 25

        distance_diag = math.sqrt(((obj_x - x) ** 2) + ((square_obj_y - square_y) ** 2))

        total_distance = total_distance + distance_diag

    avg_distance = total_distance / 10

    return avg_distance


def calculate_score(player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance, p4_avg_distance, p5_avg_distance,
                    p6_avg_distance):

    score = 0

    if player_turn == 1:
        print("-- loop player 1")
        pturn_avg_distance = p1_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 2:
        print("-- loop player 2")
        pturn_avg_distance = p2_avg_distance
        score = ((p1_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 3:
        print("-- loop player 3")
        pturn_avg_distance = p3_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p1_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 4:
        print("-- loop player 4")
        pturn_avg_distance = p4_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p1_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 5:
        print("-- loop player 5")
        pturn_avg_distance = p5_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p1_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 6:
        print("-- loop player 6")
        pturn_avg_distance = p6_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p1_avg_distance - pturn_avg_distance)) / 5

    return score



