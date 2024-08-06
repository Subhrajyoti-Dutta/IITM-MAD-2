new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        position: "",
        loading: true,
        totalInfluencers: 0,
        totalSponsors: 0,
        totalCampaigns: 0,
        flaggedInfluencers: 0,
        flaggedSponsors: 0,
        flaggedCampaigns: 0,
        flaggedAds: 0,
    },
    methods: {
        getData() {
            axios
                .get(`/api/admin_api/admin/${this.id}`)
                .then((response) => {
                    this.username = response.data.Username;
                    this.position = response.data.Position;
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching admin data:", error);
                    this.loading = false;
                });
        },
        fetchStatistics() {
            axios
                .get(`/api/admin_api/statistics`)
                .then((response) => {
                    this.totalInfluencers = response.data.totalInfluencers;
                    this.totalSponsors = response.data.totalSponsors;
                    this.totalCampaigns = response.data.totalCampaigns;
                    this.flaggedInfluencers = response.data.flaggedInfluencers;
                    this.flaggedSponsors = response.data.flaggedSponsors;
                    this.flaggedCampaigns = response.data.flaggedCampaigns;
                    this.flaggedAds = response.data.flaggedAds;
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching statistics:", error);
                    this.loading = false;
                });
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.getData();
        this.fetchStatistics();
    },
});
