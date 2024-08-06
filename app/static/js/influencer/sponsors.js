new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        averageRating: 0,
        totalEarnings: 0,
        loading: true,
        sponsors: [],
        modalSponsor: {
            Username: "",
            Full_Name: "",
            Country_Code: "",
            Phone: "",
            Company: "",
            Industry: "",
        },
    },
    methods: {
        fetchData() {
            axios
                .get(`/api/influencer_api/influencer/${this.id}`)
                .then((response) => {
                    this.username = response.data["Username"];
                    this.averageRating = response.data["Rating"];
                    this.totalEarnings = response.data["Earnings"];
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                    this.loading = false;
                });
        },
        fetchSponsors() {
            axios
                .get("/api/sponsor_api/sponsors")
                .then((response) => {
                    this.sponsors = response.data;
                })
                .catch((error) => {
                    console.error("Error fetching sponsors:", error);
                });
        },
        viewSponsor(sponsor) {
            this.modalSponsor = sponsor;
            $("#sponsorModal").modal("show");
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.fetchData();
        this.fetchSponsors();
    },
});
