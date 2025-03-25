import os

# GLOBALS
apples = [{
    'name': 'red_delicious',
    'bounds': [97,137,195,248,336,433,550],
    'sum_name': 'gdd_accumulations_1000'
},{
    'name': 'empire',
    'bounds': [97,103,186,233,297,393,500],
    'sum_name': 'gdd_accumulations_1100'
},{
    'name': 'mcIntosh',
    'bounds': [85,122,178,233,294,385,484],
    'sum_name': 'gdd_accumulations_1100'
}]

def handle_apple_data(target_dir, lat, lon, sums, min_temp):
    for apple in apples:
        gdd_sum = sums[apple['sum_name']]

        # Write gdd accumulation to relevant apple file
        with open(os.path.join(target_dir, 'apple', 'gdds', f'{apple["name"]}_data.txt'), 'a') as f:
            f.write(f'\n\t{lat}\t{lon}\t{gdd_sum}')

        # Determine phenological stage and use that and today's min temp to determine the kill probability
        kill_probs_list = [
            [-25,-25,-25],
            [11,5,0],
            [19,10,4],
            [22,17,11],
            [25,21,18],
            [27,26,24],
            [28,26,25],
            [29,27.1,26.6]
        ]
        kill_probs = kill_probs_list[-1]
        for i, boundary in enumerate(apple['bounds']):
            if gdd_sum < boundary:
                kill_probs = kill_probs_list[i]
                break
        if min_temp < kill_probs[2]:
            kill_prob = 3
        elif min_temp < kill_probs[1]:
            kill_prob = 2
        elif min_temp < kill_probs[0]:
            kill_prob = 1
        else:
            kill_prob = 0

        # Write kill probability to file
        with open(os.path.join(target_dir, 'apple', 'kill_prob', f'{apple["name"]}_data.txt'), 'a') as f:
            f.write(f'\n\t{lat}\t{lon}\t{kill_prob}')