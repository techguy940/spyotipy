import asyncio
from typing import Optional

from spotify.http import HTTP
from spotify.models import Album, Track


class Client:
    """Client Object Used to Comnunicate with Spotify API
    Parameters
    ---------
    client_id: :class:`str`
        The id of the client
    client_secret: :class:`str`
        The secret for the client

    You can get both `client_id` and `client_secret` from spotify
    developers dashboard https://developer.spotify.com/dashboard/applications
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self.loop = loop if loop is not None else asyncio.get_event_loop()

        self.http = HTTP(client_id, client_secret, loop=self.loop)

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    def __repr__(self):
        return '<Client id="{0.client_id}">'.format(self)

    @property
    def client_id(self) -> str:
        """:class:`str` - The Spotify client ID."""
        return self.http.client_id

    @property
    def client_secret(self) -> str:
        """:class:`str` - The Spotify client Secret."""
        return self.http.client_secret

    async def close(self):
        """Close the HTTP session."""
        await self.http.close()

    async def get_album(self, _id: str, *, market: str = "US") -> Album:
        """Retrieve an album with a spotify ID.
        Parameters
        ----------
        _id : :class:`str`
            The ID to search for.
        market : Optional[:class:`str`]
            An ISO 3166-1 alpha-2 country code
        Returns
        -------
        album : :class:`spotify.models.Album`
            The album retrieved from the ID
        """
        data = await self.http.get_album(_id, market=market)
        return Album(self, data)

    async def get_track(self, _id: str, *, market: str = "US"):
        """Retrieve a trach with its spotify ID.
        Parameters
        ----------
        _id : :class:`str`
            The ID to search for.
        market : Optional[:class:`str`]
            An ISO 3166-1 alpha-2 country code
        Returns
        -------
        track : :class:`spotify.models.Track`
            The track retrieved from the ID
        """
        data = await self.http.get_track(_id, market=market)
        return Track(self, data)
