from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task()
    def index(self):
        self.client.get('/')

    @task()
    def points_board(self):
        self.client.get('/points-board')

    @task()
    def show_summary(self):
        self.client.post('/show-summary', {'email': 'john@simplylift.co'})

    @task
    def purchase_places(self):
        self.client.post(
            '/purchase-places',
            {
                'club': 'Simply Lift',
                'competition': 'TM Cup',
                'places': '1',
            }
        )
