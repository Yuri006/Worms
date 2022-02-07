import sqlite3
import random
from collections import OrderedDict

Genesis_gens = ['id', 'name', 'health', 'attack', 'cryo_imm', 'in_cryo', 'immunity', 'term_imm', 'shield', 'genesis',
                'size', 'death_gen', 'anti_gen', 'fertility', 'mutant', 'term', 'birthday', 'hit', 'cryo_exp',
                'attack_exp', 'shield_exp']

# супер, мега, гипер, омега

cryo_death_k = 0.59
size_damage_k = 0.6
anti_gen_term_k = 0.1


def specific_sort(a):
    n_a = []
    for i in range(len(a)):
        if i == 0:
            n_a.append([a[i][0]])
            last = a[i][1]
        else:
            if last == a[i][1]:
                n_a[-1].append(a[i][0])
            else:
                last = a[i][1]
                n_a.append([a[i][0]])
    # print(n_a)
    return n_a


def specific_find(a, e):
    for i in range(len(a)):
        if e in a[i]:
            return i


class WormDB:
    def __init__(self, sql_path):
        self.path = sql_path

    def init_table(self):
        db = sqlite3.connect(self.path)
        cur = db.cursor()
        sql1 = """CREATE TABLE IF NOT EXISTS Users (
                            tg_id integer primary key                        
                        );"""
        sql2 = """CREATE TABLE IF NOT EXISTS Worms (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            name text DEFAULT null,
                            health integer,
                            attack integer,
                            cryo_imm integer,
                            in_cryo boolean,
                            immunity boolean,
                            term_imm integer,
                            shield integer,
                            genesis boolean,
                            size integer,
                            death_gen integer,
                            anti_gen,
                            fertility integer,
                            mutant integer,
                            term integer,
                            birthday text,
                            hit integer,
                            cryo_exp integer, 
                            attack_exp integer,
                            shield_exp integer
                        );"""
        command = [cur.execute(i) for i in [sql1, sql2]]
        db.commit()

    def add_user(self, id):
        db = sqlite3.connect(self.path)
        cur = db.cursor()
        sql1 = " INSERT INTO Users(tg_id) VALUES(?)"
        cur.execute(sql1, (id,))
        db.commit()
        sql1 = """CREATE TABLE IF NOT EXISTS """ + 'u_' + str(id) + """ (
                            worm_id integer                      
                        );"""
        cur.execute(sql1)
        db.commit()

    def create_worm(self, *args):
        db = sqlite3.connect(self.path)
        cur = db.cursor()
        sql = ''' INSERT INTO Worms(name, health, attack, cryo_imm, in_cryo, immunity, term_imm, shield, genesis, size, death_gen, anti_gen, fertility, mutant, term, birthday, hit, cryo_exp, attack_exp, shield_exp) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'), ?, ?, ?, ?) '''
        cur.execute(sql, args)
        db.commit()
        sql1 = "SELECT last_insert_rowid()"
        cur.execute(sql1)
        worm_id = cur.fetchall()[0][0]
        return worm_id

    def get_users_worm(self, tg_id):
        u_worms = []
        db = sqlite3.connect(self.path)
        cur = db.cursor()
        sql1 = "SELECT worm_id FROM " + 'u_' + str(tg_id)
        cur.execute(sql1)
        db.commit()
        x = cur.fetchall()
        for worm_id in x:
            u_worms.append([])
            sql = '''SELECT * FROM Worms WHERE id = ?'''
            # print(worm_id, sql)
            cur.execute(sql, (int(worm_id[0]),))
            db.commit()
            worm_by_id = cur.fetchall()
            u_worms[-1] += list(worm_by_id[0])
        return u_worms

    def add_worm_to(self, tg_id, worm_id):
        db = sqlite3.connect(self.path)
        cur = db.cursor()
        sql1 = " INSERT INTO " + 'u_' + str(tg_id) + "(worm_id) VALUES(?)"
        cur.execute(sql1, (worm_id,))
        db.commit()

    def create_genesis_worm(self):
        # id, name, health, attack, cryo_imm, in_cryo, immunity, term_imm, shield, genesis, size, death_gen, anti_gen, fertility, mutant, term, birthday, hit, cryo_exp, attack_exp, shield_exp
        health = round(random.uniform(0.08, 0.3), 2)
        worm_id = self.create_worm('Генезисный червь',
                                   health,
                                   round(random.uniform(0.001, 0.01), 3),
                                   round(random.uniform(0.001, 0.005), 3),
                                   False,
                                   True,
                                   round(random.uniform(0.0001, 0.0007), 4),
                                   round(random.uniform(0.0001, 0.0007), 4),
                                   True,
                                   0.001,
                                   round(random.uniform(0.001, 0.005), 3),
                                   round(random.uniform(0.001, 0.005), 3),
                                   round(random.uniform(0.001, 0.005), 3),
                                   round(random.uniform(0.0001, 0.0007), 4),
                                   0,
                                   health,
                                   0,
                                   0,
                                   0
                                   )
        return worm_id

    def update_gen(self, worm_id):
        pass

    def kill_worm(self, worm_id):
        pass

    def get_stats_of_gen(self, gen):
        db = sqlite3.connect(self.path)
        cur = db.cursor()
        sql = "SELECT id, " + gen + " FROM Worms ORDER BY " + gen
        cur.execute(sql)
        db.commit()
        s = cur.fetchall()
        return s

    def worms_gens_stats(self, worm_id):
        number_of_worms = len(self.get_stats_of_gen('id'))
        w_s = []
        for gen in Genesis_gens[2:-6]:
            g_s = specific_sort(self.get_stats_of_gen(gen))
            w_s.append((specific_find(g_s, worm_id) + 1) / len(g_s))
        return dict(zip(Genesis_gens[2:-6], w_s))


class Worm:
    def __init__(self, gens):
        self.gens = dict(zip(Genesis_gens, gens))
        self.my_id = self.gens['id']

    def __getitem__(self, item):
        return self.gens[item]

    def print_gen(self):
        for i in self.gens:
            print(i + ': ' + str(self.gens[i]))

    def death_gen(self):
        if random.randint(1, 10000) <= (self.gens['death_gen'] * 10000):
            return 1
        return 0

    def cryogen(self):
        if not self.death_gen():
            self.gens['in_cryo'] = 1
            return 1, 0
        else:
            return 0, 'gen'

    @property
    def domain_gen_stats(self):
        my_stats = g.worms_gens_stats(self.my_id)
        my_stats['death_gen'] = 1 - my_stats['death_gen']
        my_stats['anti_gen'] = 1 - my_stats['anti_gen']
        my_stats.pop('genesis')
        my_stats.pop('immunity')
        my_stats.pop('in_cryo')
        return dict(sorted(my_stats.items(), key=lambda item: item[1]))

    def defrosting(self):
        gen = self.death_gen()
        cryo = random.randint(1, 10000) <= cryo_death_k * (1 - self.gens['cryo_imm']) * 10000
        if not gen and not cryo:
            self.gens['in_cryo'] = 0
            self.gens['cryo_exp'] += 1 * (1 + self.gens['mutant'])
            return 1, 0
        elif gen and cryo:
            return 0, 2
        elif gen:
            return 0, 1
        else:
            return 0, 0

    def term_damage(self, d_t):
        gen = self.death_gen()
        if not gen and not self.gens['in_cryo']:
            self.gens['term'] += d_t
            self.gens['hit'] -= abs(d_t) * (1 + self.gens['anti_gen'] * anti_gen_term_k - self.gens['cryo_imm'])
            if self.gens['hit'] <= 0:
                return 0
            return 1
        if gen:
            return 1
        return 0

    def attack(self, other):
        gen = self.death_gen()
        damage = self.gens['attack'] * (1 + (self.gens['size'] - other.gens['size']) * size_damage_k) - other.gens[
            'shield']
        self.gens['attack_exp'] += 1 * (1 + other.gens['mutant'])
        if other.gens['hit'] - damage <= 0:
            # attacker, defender
            return int(not gen), 0
        else:
            other.gens['hit'] -= damage
            other.gens['shield_exp'] += 1 * (1 + other.gens['mutant'])
            return int(not gen), 1

    def crossing(self, other):
        if self.gens['genesis'] == 1 and other.gens['genesis'] == 1:
            pass
        else:
            child_q = 2 + (self.gens['fertility'] + other.gens['fertility'])
            pass

# recurrent

g = WormDB('worms.db')

# g.init_table()
# g.add_user(11)

# p1 = [g.add_worm_to(11, g.create_genesis_worm()) for i in range(10)]


# print(g.get_stats_of_gen('health'))

# stats = g.worms_gens_stats(1)
user_w = []
for w in g.get_users_worm(11):
    user_w.append(Worm(w))

stats = user_w[4].domain_gen_stats
for i in stats:
    print(i + ': ' + str(stats[i]))
print('--------------')
user_w[4].print_gen()

'''
user_w = []
for w in g.get_users_worm(11):
    user_w.append(Worm(w))
# print(user_w[0]['cryo_imm'])

all_result = {}
death_gens = 0
for j in range(20000):
    for i in range(100):
        if not user_w[1].cryogen()[0]:
            death_gens += 1
            break
        d = user_w[1].defrosting()
        if not d[0]:
            if d[1] == 1 or d[1] == 2:
                death_gens += 1
            if d[1] == 0 or d[1] == 2:
                if i not in all_result:
                    all_result[i] = 1
                else:
                    all_result[i] += 1
            break


for i in dict(sorted(all_result.items())):
    print(i, 'times in cryo:', all_result[i])
print('killed by death gen:', death_gens)
print('------------------------')
user_w[1].print_gen()
'''
