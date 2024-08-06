new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        company: "",
        budget: 0,
        loading: true,
        influencers: [],
        modalInfluencer: { Platform: {} },
    },
    methods: {
        fetchData() {
            axios
                .get(`/api/sponsor_api/sponsor/${this.id}`)
                .then((response) => {
                    this.username = response.data["Username"];
                    this.company = response.data["Company"];
                    this.budget = response.data["Budget"];
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                    this.loading = false;
                });
        },
        fetchInfluencers() {
            axios
                .get(`/api/influencer_api/influencers`)
                .then((response) => {
                    console.log(response.data);
                    this.influencers = response.data;
                })
                .catch((error) => {
                    console.error("Error fetching influencers:", error);
                });
        },
        viewInfluencer(influencer) {
            this.modalInfluencer = influencer;
            $("#influencerModal").modal("show");
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.fetchData();
        this.fetchInfluencers();
    },
});
