const app = Vue.createApp({
  data() {
    return {
      activeTab: "artists",
      artists: [],
      albums: [],
      tracks: [],
      showArtistForm: false,
      showAlbumForm: false,
      showTrackForm: false,
      formData: {},
      apiUrl: "http://127.0.0.1:8000/",
    };
  },
  methods: {
    async loadEntities(entity) {
      const response = await axios.get(`${this.apiUrl}${entity}/`);
      console.log("Loaded data:", response.data);
      this[entity] = response.data.data;
    },
    async saveEntity() {
      const entity = this.showArtistForm
        ? "artists"
        : this.showAlbumForm
        ? "albums"
        : "tracks";
      if (this.formData.id) {
        await axios.put(`${this.apiUrl}${entity}/${this.formData.id}`, this.formData);
      } else {
        await axios.post(`${this.apiUrl}${entity}/`, this.formData);
      }
      this.closeForm();
      await this.loadEntities(entity);
    },
    async deleteEntity(entity, id) {
      if (!id) {
        console.error(`Invalid ID for ${entity}: ${id}`);
        return;
      }
      await axios.delete(`${this.apiUrl}${entity}/${id}`);
      this.loadEntities(entity);
    },
    editEntity(entity, data) {
      this.formData = { ...data };
      if (entity === "artists") this.showArtistForm = true;
      if (entity === "albums") this.showAlbumForm = true;
      if (entity === "tracks") this.showTrackForm = true;
    },
    closeForm() {
      this.formData = {};
      this.showArtistForm = this.showAlbumForm = this.showTrackForm = false;
    },
    async deleteArtist(id) {
      this.deleteEntity("artists", id);
    },
    async deleteAlbum(id) {
      this.deleteEntity("albums", id);
    },
    async deleteTrack(id) {
      this.deleteEntity("tracks", id);
    },
    editArtist(artist) {
      this.editEntity("artists", artist);
    },
    editAlbum(album) {
      this.editEntity("albums", album);
    },
    editTrack(track) {
      this.editEntity("tracks", track);
    },
    getArtistName(artistId) {
      const artist = this.artists.find(a => a.artist_id === artistId);
      return artist ? artist.name : "Неизвестный артист";
    },
    getAlbumName(albumId) {
      const album = this.albums.find(a => a.album_id === albumId);
      return album ? album.name : "Неизвестный альбом";
    },
    switchTab(tab) {
      this.activeTab = tab;
      localStorage.setItem("activeTab", tab);
    },
  },
  mounted() {
    const savedTab = localStorage.getItem("activeTab");
    if (savedTab) {
      this.activeTab = savedTab;
    }
    this.loadEntities("artists");
    this.loadEntities("albums");
    this.loadEntities("tracks");
  },
});

app.mount("#app");
