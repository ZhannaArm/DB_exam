const app = Vue.createApp({
  data() {
    return {
      activeTab: "artists",
      artists: [],
      albums: [],
      tracks: [],
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      showArtistForm: false,
      showAlbumForm: false,
      showTrackForm: false,
      formData: {},
      apiUrl: "http://127.0.0.1:8000/",
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    },
  },
  methods: {
    async loadEntities(entity) {
      const skip = (this.currentPage - 1) * this.itemsPerPage;
      const limit = this.itemsPerPage;

      try {
        const response = await axios.get(`${this.apiUrl}${entity}/`, {
          params: { skip, limit },
        });

        console.log(`Loaded ${entity}:`, response.data);

        this[entity] = response.data.data;
        this.totalItems = response.data.total_count;
      } catch (error) {
        console.error(`Error loading ${entity}:`, error);
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.loadEntities(this.activeTab);
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.loadEntities(this.activeTab);
      }
    },
    async saveEntity() {
      const entity = this.showArtistForm
        ? "artists"
        : this.showAlbumForm
        ? "albums"
        : "tracks";

      if (this.showTrackForm) {
        this.formData.track_metadata = {};
        if (this.formData.rating) this.formData.track_metadata.rating = this.formData.rating;
        if (this.formData.instruments) this.formData.track_metadata.instruments = this.formData.instruments;

        if (Object.keys(this.formData.track_metadata).length === 0) {
          this.formData.track_metadata = null;
        }
      }

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
      await this.loadEntities(entity);
    },
    editEntity(entity, data) {
      this.formData = { ...data };
      if (entity === "tracks" && this.formData.track_metadata) {
        this.formData.rating = this.formData.track_metadata.rating || null;
        this.formData.instruments = this.formData.track_metadata.instruments || null;
      }
      if (entity === "artists") this.showArtistForm = true;
      if (entity === "albums") this.showAlbumForm = true;
      if (entity === "tracks") this.showTrackForm = true;
    },
    closeForm() {
      this.formData = {};
      this.showArtistForm = this.showAlbumForm = this.showTrackForm = false;
    },
    async deleteArtist(id) {
      await this.deleteEntity("artists", id);
    },
    async deleteAlbum(id) {
      await this.deleteEntity("albums", id);
    },
    async deleteTrack(id) {
      await this.deleteEntity("tracks", id);
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
    switchTab(tab) {
      this.activeTab = tab;
      this.currentPage = 1;
      localStorage.setItem("activeTab", tab);
      this.loadEntities(this.activeTab);
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
