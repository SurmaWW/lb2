import alch
from sqlalchemy import Column, Integer, String


class Performer(alch.Base):
    __tablename__ = 'Performer'
    Artist_ID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    genre = Column(String, nullable=True)


class ModelPerformer:
    def __init__(self, db_model):
        self.conn = db_model.conn
        self.engine = alch.create_engine(alch.DATABASE_URL)
        self.session = alch.Session.configure(bind=self.engine)
        self.session = alch.Session()

    def add_Performer(self, Artist_ID, name, surname, genre):
        try:
            new_performer = Performer(
                Artist_ID=Artist_ID,
                name=name,
                surname=surname,
                genre=genre
            )
            self.session.add(new_performer)
            self.session.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Adding A Performer: {str(e)}")
            return False   # Returns False if insertion fails

    def get_all_Performers(self):
        c = self.session.cursor()
        c.execute('SELECT * FROM "Performer"')
        return c.fetchall()

    def update_Performer(self, Artist_ID, name, surname, genre):
        try:
            performer = self.session.query(Performer).filter_by(Artist_ID=Artist_ID).first()

            if performer:
                performer.Artist_ID = Artist_ID
                performer.name = name
                performer.surname = surname
                performer.genre = genre

                self.session.commit()
                return True  # Returns True if the update was successful
            else:
                return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With A Performer Updating: {str(e)}")
            return False   # Returns False if insertion fails

    def delete_Performer(self, Artist_ID):
        try:
            performer = self.session.query(Performer).filter_by(Artist_ID=Artist_ID).first()

            if performer:
                self.session.delete(performer)
                self.session.commit()
                return True  # Returns True if the update was successful
            else:
                return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With An Artist Deleting: {str(e)}")
            return False  # Returns False if insertion fails

    def check_Performer_existence(self, Artist_ID):
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM "Performer" WHERE "Artist_ID" = %s', (Artist_ID,))
        return c.fetchone() is not None

    def create_Performer_sequence(self):
        # Check for the existence of a sequence
        c = self.conn.cursor()
        c.execute("""
            DO $$
           BEGIN
               IF NOT EXISTS(SELECT 1 FROM pg_sequences WHERE schemaname='public' AND sequencename='artist_id_seq') THEN
                   CREATE SEQUENCE artist_id_seq;
               ELSE
                   DROP SEQUENCE artist_id_seq;
                   CREATE SEQUENCE artist_id_seq;
               END IF;
           END $$;
        """)
        self.conn.commit()

    def generate_rand_Performer_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""
            INSERT INTO "Performer" ("Artist_ID" ,"name", "surname", "genre")
            SELECT
                nextval('artist_id_seq'), 
                (array['Ivan', 'Mike', 'John', 'Harry'])[floor(random() * 4) + 1],
                (array['Lenon', 'Muller', 'Vachovski', 'Potter'])[floor(random() * 4) + 1],
                (array['Rock', 'Jazz', 'All', 'Pop'])[floor(random() * 4) + 1]     
            FROM generate_series(1, %s);
            """, (number_of_operations,))
            self.conn.commit()
            return True  # Returns True if the insertion was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error With A Performer Adding: {str(e)}")
            return False   # Returns False if insertion fails

    def truncate_Performer_table(self):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""DELETE FROM "Performer" """)
            self.conn.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error With A Performer`s Data Deleting: {str(e)}")
            return False   # Returns False if insertion fails