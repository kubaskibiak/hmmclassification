class Observation:
    num_faces = 0
    is_close = False
    is_in_DB = False
    is_in_last_shot = 0
    is_first_frame=False
    symbol = ''

    def __init__(self, num_faces=0, is_close=False, is_in_db=False, is_in_last_shot=0, is_first_frame=False):
        self.num_faces = num_faces
        self.is_close = is_close
        self.is_in_db = is_in_db
        self.is_in_last_shot = is_in_last_shot
        self.is_first_frame = is_first_frame
        self.symbol = self.find_symbol()

    def find_symbol(self):
        if self.is_first_frame is True:
            return 'Pierwsza klatka w ujęciu'

        if self.num_faces == 0:
            return 'Brak osób na ujęciu'

        elif self.num_faces == 1:
            if self.is_close is True:
                if self.is_in_db is True:
                    if self.is_in_last_shot==1:
                        return 'Jedna osoba, która była już wcześniej - ujęcie ze zbliżeniem, była 1 ujęcie wcześniej'
                    elif self.is_in_last_shot == 2:
                        return 'Jedna osoba, która była już wcześniej - ujęcie ze zbliżeniem, była 2 ujęcia wcześniej'
                    else:
                        return 'Jedna osoba, która była już wcześniej - ujęcie ze zbliżeniem, była conajmniej 3 ujęcia wcześniej'
                else:
                    return 'Jedna osoba, której nie było  wcześniej - ujęcie ze zbliżeniem'

            else:
                if self.is_in_db is True:
                    if self.is_in_last_shot==1:
                        return 'Jedna osoba, która była już  wcześniej - ujęcie BEZ zbliżenia, była 1 ujęcie wcześniej'
                    elif self.is_in_last_shot == 2:
                        return 'Jedna osoba, która była już  wcześniej - ujęcie BEZ zbliżenia,  była 2 ujęcia wcześniej'
                    else:
                        return 'Jedna osoba, która była już  wcześniej - ujęcie BEZ zbliżenia,  była conajmniej 3 ujęcia wcześniej'


                else:
                    return 'Jedna osoba, której nie było  wcześniej - ujęcie BEZ zbliżenia'

        elif self.num_faces > 1:

            if self.is_close is True:
                if self.is_in_db is True:
                    if self.is_in_last_shot ==1:
                        return 'Wiele osób, wsytępuje zbliżenia na conajmniej 1, conajmniej 1 już była wczesniej, była 1 ujęcie wcześniej'
                    elif self.is_in_last_shot == 2:
                        return 'Wiele osób, wsytępuje zbliżenia na conajmniej 1, conajmniej 1 już była wczesniej, była 2 ujęcia wcześniej'
                    else:
                        return 'Wiele osób, wsytępuje zbliżenia na conajmniej 1, conajmniej 1 już była wczesniej, była conajmniej 3 ujęcia wcześniej'

                else:
                    return 'Wiele osób, wsytępuje zbliżenia na conajmniej 1, żadna NIE była wczesniej'

            else:
                if self.is_in_db is True:
                    if self.is_in_last_shot == 1:
                        return 'Wiele osób, Brak zbliżenia, conajmniej 1 już była wczesniej, była 1 ujęcie wcześniej'
                    elif self.is_in_last_shot == 2:
                        return 'Wiele osób, Brak zbliżenia, conajmniej 1 już była wczesniej, była 2 ujęcia wcześniej'
                    else:
                        return 'Wiele osób, Brak zbliżenia, conajmniej 1 już była wczesniej, była conajmniej 3 ujęcia wcześniej'
                else:
                    return 'Wiele osób, Brak zbliżenia, żadna NIE była wczesniej'

    def __str__(self):
        return self.symbol