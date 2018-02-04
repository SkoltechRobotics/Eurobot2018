class CubePickingOptimizer:
    def __init__(self):
        self.Allowed_seq_1 = []
        self.Allowed_seq_2 = []
        self.Allowed_seq_3 = []

    def set_plan(self, plan):
        self.allowed_cubes_seq(plan)

    def allowed_cubes_seq(self, plan):
        all_cubes = list(range(5))
        oth = list(set(all_cubes) - set(plan))
        sds = [plan[0], plan[2]]
        cnt = plan[1]

        self.Allowed_seq_1 = [
            (oth[0],),
            (oth[1],),
            (sds[0],),
            (sds[1],)
        ]

        self.Allowed_seq_2 = [
            (oth[0], sds[0]),
            (oth[1], sds[0]),
            (oth[0], sds[1]),
            (oth[1], sds[1]),
            (oth[0], oth[1]),
            (oth[1], oth[0]),
            (sds[1], cnt),
            (sds[0], cnt)
        ]

        self.Allowed_seq_3 = [
            (oth[0], sds[0], cnt),
            (oth[1], sds[0], cnt),
            (oth[0], sds[1], cnt),
            (oth[1], sds[1], cnt),
            (oth[0], oth[1], sds[0]),
            (oth[0], oth[1], sds[1]),
            (oth[1], oth[0], sds[0]),
            (oth[1], oth[0], sds[1]),
            (cnt, sds[0], oth[0]),
            (cnt, sds[0], oth[1]),
            (cnt, sds[1], oth[0]),
            (cnt, sds[1], oth[1]),
            (sds[0], oth[0], oth[1]),
            (sds[1], oth[0], oth[1]),
            (sds[0], oth[1], oth[0]),
            (sds[1], oth[1], oth[0]),
            (sds[1], cnt, sds[0]),
            (sds[0], cnt, sds[1])
        ]

    def find_optimal_sequence(self, key):
        # dynamic searching of optimal piking sequence
        seqs = [{((), (), ()): []}, {}, {}, {}]
        for i in range(3):
            for last_picked_cubes, last_seq in seqs[i].items():
                for new_picked_cubes, new_seq in self.pick_one_heap(last_picked_cubes, last_seq):
                    if self.check_safety(new_picked_cubes, i + 1):
                        old_value = seqs[i + 1].get(new_picked_cubes)
                        if old_value is None:
                            seqs[i + 1][new_picked_cubes] = new_seq
                        else:
                            seqs[i + 1][new_picked_cubes] = min(new_seq, seqs[i + 1][new_picked_cubes], key=key)
        return min(seqs[3].values(), key=key)

    def pick_one_heap(self, picked_cubes, seq):
        remain_cubes = [0, 1, 2, 3]
        yield from self.pick_one_cube(picked_cubes, seq, [3, 4, 1], remain_cubes)
        yield from self.pick_one_cube(picked_cubes, seq, [2, 1, 4, 1], remain_cubes)
        yield from self.pick_one_cube(picked_cubes, seq, [2, 2, 4], remain_cubes)
        yield from self.pick_one_cube(picked_cubes, seq, [1, 2, 4, 1], remain_cubes)
        yield from self.pick_one_cube(picked_cubes, seq, [1, 1, 1, 4, 1], remain_cubes)

    def check_safety(self, towers_cubes, n):
        n_tr = 0
        for tower in towers_cubes:
            if len(tower) > 3 and tower[-3:] in self.Allowed_seq_3[8:]:
                n_tr += 1
        return n_tr >= n

    def check_tower(self, tower_cubes):
        n = len(tower_cubes)
        if n == 1:
            return tower_cubes in self.Allowed_seq_1
        elif n == 2:
            return tower_cubes in self.Allowed_seq_2
        elif n < 6:
            return tower_cubes[-3:] in self.Allowed_seq_3
        else:
            return False

    @staticmethod
    def pick(remain_cubes, n_cubes):
        if n_cubes == 4:
            for i in range(3):
                picked_cubes = [[], [], []]
                picked_cubes[i] = [4]
                yield remain_cubes, picked_cubes, [i]
        elif n_cubes == 1:
            for i in range(len(remain_cubes)):
                for j in range(3):
                    picked_cubes = [[], [], []]
                    picked_cubes[j] = [remain_cubes[i]]
                    yield remain_cubes[:i] + remain_cubes[i + 1:], picked_cubes, [j]
        elif n_cubes == 2:
            for i in range(4):
                picked = [i, (i + 1) % 4]
                if all([(x in remain_cubes) for x in picked]):
                    yield list(set(remain_cubes) - set(picked)), [[picked[0]], [picked[1]], []], [0, 1]
                    yield list(set(remain_cubes) - set(picked)), [[], [picked[0]], [picked[1]]], [1, 2]
            for i in range(4):
                picked = [i, (i + 2) % 4]
                if all([(x in remain_cubes) for x in picked]):
                    yield list(set(remain_cubes) - set(picked)), [[picked[0]], [], [picked[1]]], [0, 2]
        elif n_cubes == 3:
            yield [3], [[0], [1], [2]], [0, 1, 2]
            yield [0], [[1], [2], [3]], [0, 1, 2]
            yield [1], [[2], [3], [0]], [0, 1, 2]
            yield [2], [[3], [0], [1]], [0, 1, 2]

    def pick_one_cube(self, picked_cubes, seq, strat, remain_cubes):
        if strat:
            for new_remain_cubes, new_picked_cubes, towers in self.pick(remain_cubes, strat[0]):
                new_towers_cubes = tuple([picked_cubes[i] + tuple(new_picked_cubes[i]) for i in range(3)])
                if all([self.check_tower(new_towers_cubes[x]) for x in towers]):
                    yield from self.pick_one_cube(new_towers_cubes, seq + [new_picked_cubes], strat[1:],
                                                  new_remain_cubes)
        else:
            yield picked_cubes, seq

    @staticmethod
    def picking_places_and_states(seq):
        places = []
        states = []
        for i, pick in enumerate(seq):
            n = sum(map(lambda x: len(x), pick))
            place = 0
            state = 0
            for j, cube in enumerate(pick):
                if cube:
                    if cube[0] == 4:
                        state = 1
                        place = places[-1]
                    elif len(states) != 0 and states[-1] == 1 and n == 1:
                        place = places[-1] = (cube[0] - j - 1) % 4
                        state = 2
                    else:
                        place = (cube[0] - j + 1) % 4
                        state = 0
                    break
            places.append(place)
            states.append(state)
        return places, states

    @staticmethod
    def dif_point(x1, x2, n):
        return min((x1 - x2) % n, (x1 - x2) % n)

    def rotation_time(self, places, states, start_points=None):
        if start_points is not None:
            time = self.dif_point(start_points[0], places[0], 4)
            n_start = 1
        else:
            time = 0
            n_start = 0
        for i in range(len(places)):
            if i != 0 and not (states[i] == 0 and states[i - 1] != 0):
                time += min((places[i] - places[i - 1]) % 4, (places[i - 1] - places[i]) % 4)
            elif i != 0 and states[i] == 0 and states[i - 1] != 0 and start_points is not None:
                time += self.dif_point(start_points[n_start], places[i], 4)
                n_start += 1
        return time

    @staticmethod
    def move_time(places, states):
        time = 0
        for i in range(len(places)):
            if i != 0 and (states[i] == 1 and states[i - 1] == 0 or states[i] == 2 and states[i - 1] == 1):
                time += 1
        return time

    def get_fun_time(self, k_r=1, k_m=1, k_p=1, start_points=None):
        def time(seq):
            places, states = self.picking_places_and_states(seq)
            t_r = self.rotation_time(places, states, start_points)
            t_m = self.move_time(places, states)
            t_p = len(seq)
            return t_r * k_r + t_m * k_m + t_p * k_p
        return time
