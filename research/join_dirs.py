import os
import shutil
from research.leaves import get_game_move_id
from research.saver import parse_to_file_name

if __name__ == '__main__':
    src_dir = '../outcomes_to_process/2019-04-04-171236'
    dst_dir = '../outcomes_to_process/2019-04-04-123018'

    next_game_id = None
    files = os.listdir(dst_dir)
    files.sort()
    for file_name in files:
        game_id, move_id = get_game_move_id(file_name)
        next_game_id = int(game_id)

    src_files = os.listdir(src_dir)
    src_files.sort()
    last_game_id = 0
    for file_name in src_files:
        game_id, move_id = get_game_move_id(file_name)
        if last_game_id != game_id:
            last_game_id = game_id
            next_game_id += 1
        new_file_name = parse_to_file_name(next_game_id, move_id)

        src_file_path = os.path.join(src_dir, file_name)
        dst_file_path = os.path.join(dst_dir, new_file_name)
        os.rename(src_file_path, dst_file_path)