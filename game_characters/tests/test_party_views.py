from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from game_characters.models import Party

User = get_user_model()

class PartyViewTests(TestCase):
    def setUp(self):
        # Create DM and players
        self.dm = User.objects.create_user(username="dm_user", password="testpass")
        self.player1 = User.objects.create_user(username="player1", password="testpass")
        self.player2 = User.objects.create_user(username="player2", password="testpass")

        # Create a party owned by DM
        self.party = Party.objects.create(name="Dungeon Raiders", dungeon_master=self.dm)
        self.party.members.add(self.player1)

        # Auth client as DM by default
        self.client = Client()
        self.client.login(username="dm_user", password="testpass")

    def test_dm_can_invite_member(self):
        """Dungeon Master can invite a new player by username."""
        url = reverse("party_invite", args=[self.party.pk])
        response = self.client.post(url, {"username": "player2"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.player2, self.party.members.all())

    def test_dm_cannot_invite_nonexistent_user(self):
        """DM gets error message when inviting non-existent user."""
        url = reverse("party_invite", args=[self.party.pk])
        response = self.client.post(url, {"username": "ghost_user"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("ghost_user", [u.username for u in self.party.members.all()])

    def test_non_dm_cannot_invite(self):
        """Non-DMs should be blocked from inviting members."""
        self.client.logout()
        self.client.login(username="player1", password="testpass")
        url = reverse("party_invite", args=[self.party.pk])
        response = self.client.post(url, {"username": "player2"}, follow=True)
        self.assertNotIn(self.player2, self.party.members.all())

    def test_dm_can_remove_member(self):
        """Dungeon Master can remove a member from the party."""
        url = reverse("party_remove_member", args=[self.party.pk])
        response = self.client.post(url, {"member_id": self.player1.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.player1, self.party.members.all())

    def test_non_dm_cannot_remove_member(self):
        """Non-DMs cannot remove members."""
        self.client.logout()
        self.client.login(username="player1", password="testpass")
        url = reverse("party_remove_member", args=[self.party.pk])
        response = self.client.post(url, {"member_id": self.dm.id}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.dm, [self.party.dungeon_master])
