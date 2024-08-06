new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        position: "",
        loading: true,
        influencers: [],
        modalInfluencer: {},
    },
    methods: {
        getData() {
            axios
                .get(`/api/admin_api/admin/${this.id}`)
                .then((response) => {
                    this.username = response.data.Username;
                    this.position = response.data.Position;
                })
                .catch((error) => {
                    console.error("Error fetching admin data:", error);
                    this.loading = false;
                });
        },
        fetchInfluencers() {
            axios
                .get("/api/admin_api/influencers")
                .then((response) => {
                    this.influencers = response.data;
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching influencers:", error);
                    this.loading = false;
                });
        },
        viewInfluencer(influencer) {
            this.modalInfluencer = influencer;
            $("#influencerModal").modal("show");
        },
        flagInfluencer(influencerId) {
            axios
                .put(`/api/admin_api/influencer/${influencerId}`, {
                    Flag: true,
                })
                .then((response) => {
                    this.modalInfluencer.Flag = true;
                    this.updateInfluencerInList(influencerId, true);
                })
                .catch((error) => {
                    console.error("Error flagging influencer:", error);
                });
        },
        deflagInfluencer(influencerId) {
            axios
                .put(`/api/admin_api/influencer/${influencerId}`, {
                    Flag: false,
                })
                .then((response) => {
                    this.modalInfluencer.Flag = false;
                    this.updateInfluencerInList(influencerId, false);
                })
                .catch((error) => {
                    console.error("Error deflagging influencer:", error);
                });
        },
        updateInfluencerInList(influencerId, flag) {
            const influencer = this.influencers.find(
                (i) => i.Influencer_ID === influencerId
            );
            if (influencer) {
                influencer.Flag = flag;
            }
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.getData();
        this.fetchInfluencers();
    },
});
