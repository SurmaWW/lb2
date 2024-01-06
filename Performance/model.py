import alch
from sqlalchemy import Column, Integer, Date


class perfomance(alch.Base):
    __tablename__ = 'Perfomance'
    Prefomance_ID = Column(Integer, primary_key=True)
    Festival_ID = Column(Integer, nullable=False)
    Artist_ID = Column(Integer, nullable=False)
    Start_time = Column(Date, nullable=False)
    Finish_time = Column(Date, nullable=False)


class ModelPerformance:
    def __init__(self, db_model):
        self.conn = db_model.conn
        self.engine = alch.create_engine(alch.DATABASE_URL)
        self.session = alch.Session.configure(bind=self.engine)
        self.session = alch.Session()

    def add_Performance(self, Preformance_ID, Festival_ID, Artist_ID, Start_time, Finish_time):
        try:
            new_performance = perfomance(
                Performance_ID=Preformance_ID,
                Festival_ID=Festival_ID,
                Artist_ID=Artist_ID,
                Start_time=Start_time,
                Finish_time=Finish_time
            )
            self.session.add(new_performance)
            self.session.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.session.rollback()
            print(f"Error With Adding A Performance: {str(e)}")
            return False

    def get_all_Performance(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Perfomance"')
        return c.fetchall()

    def update_Performance(self, Preformance_ID, Festival_ID, Artist_ID, Start_time, Finish_time):
        try:
            Perfomance = self.session.query(perfomance).filter_by(Prefomance_ID=Preformance_ID).first()

            if Perfomance:
                Perfomance.Preformance_ID = Preformance_ID
                Perfomance.Festival_ID = Festival_ID
                Perfomance.Artist_ID = Artist_ID
                Perfomance.Start_time = Start_time
                Perfomance.Finish_time = Finish_time

                self.session.commit()
                return True  # Returns True if the update was successful
            else:
                return False
        except Exception as e:
            # Handling an error if the update failed
            self.session.rollback()
            print(f"Error With Updating A Performance: {str(e)}")
            return False   # Returns False if insertion fails

    def delete_Performance(self, Performance_ID):
        c = self.conn.cursor()
        try:
            # Attempting to update a record
            c.execute('DELETE FROM "Perfomance" WHERE "Preformance_ID"=%s', (Performance_ID,))
            self.conn.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            # Handling an error in case the deletion failed
            self.conn.rollback()
            print(f"Error With Deleting A Performance: {str(e)}")
            return False   # Returns False if insertion fails

    def check_Performance_existence(self, Performance_ID):
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM "Perfomance" WHERE "Preformance_ID" = %s', (Performance_ID,))
        return bool(c.fetchone())

    def create_Performance_sequence(self):
        c = self.conn.cursor()
        c.execute("""
           DO $$
           BEGIN
               IF NOT EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = 'perfomance_id_seq') THEN
                   CREATE SEQUENCE perfomance_id_seq;
               ELSE
                   DROP SEQUENCE perfomance_id_seq;
                   CREATE SEQUENCE perfomance_id_seq;
               END IF;
           END $$;
           """)
        self.conn.commit()

    def generate_rand_Performance_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            c.execute("""
            INSERT INTO "Perfomance" ("Preformance_ID", "Festival_ID", "Artist_ID", "Start_time", "Finish_time")
            select * from (
            SELECT
                    nextval('perfomance_id_seq'),
                    floor(random() * (SELECT max("Festival_ID") FROM "Festival") + 1),
                    floor(random() * (SELECT max("Artist_ID") FROM "Performer") + 1),
                    ('2023-01-01'::date + floor(random() * 3) * interval '1 day' + floor(random() * 12) * interval '1 month' + floor(random() * 31) * interval '1 day') as begin1,
                    ('2023-01-01'::date + floor(random() * 3) * interval '1 day' + floor(random() * 12) * interval '1 month' + floor(random() * 31) * interval '1 day') as end1
                FROM generate_series(1, %s)) as t
            WHERE begin1 < end1
                  """, (number_of_operations,))

            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Creating A Performance: {str(e)}")
            return False


    def truncate_Performance_table(self):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""DELETE FROM "Perfomance" """)
            self.conn.commit()
            return True  # Returns True if the insertion was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Deleting A Performance Data: {str(e)}")
            return False  # Returns False if insertion fails