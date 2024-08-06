new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        position: "",
        loading: true,
        sponsors: [],
        modalSponsor: {},
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
                    console.error("Error fetching sponsors:", error);
                    this.loading = false;
                });
        },
        fetchSponsors() {
            axios
                .get("/api/admin_api/sponsors")
                .then((response) => {
                    this.sponsors = response.data;
                    this.loading = false;
                })
                .catch((error) => {
                    console.error("Error fetching sponsors:", error);
                    this.loading = false;
                });
        },
        viewSponsor(sponsor) {
            this.modalSponsor = sponsor;
            $("#sponsorModal").modal("show");
        },
        flagSponsor(sponsorId) {
            console.log("flag = true");
            axios
                .put(`/api/admin_api/sponsor/${sponsorId}`, { Flag: true })
                .then((response) => {
                    this.modalSponsor.Flag = true;
                    this.updateSponsorInList(sponsorId, true);
                })
                .catch((error) => {
                    console.error("Error flagging sponsor:", error);
                });
        },
        deflagSponsor(sponsorId) {
            console.log("flag = false");
            axios
                .put(`/api/admin_api/sponsor/${sponsorId}`, { Flag: false })
                .then((response) => {
                    this.modalSponsor.Flag = false;
                    this.updateSponsorInList(sponsorId, false);
                })
                .catch((error) => {
                    console.error("Error deflagging sponsor:", error);
                });
        },
        updateSponsorInList(sponsorId, flag) {
            const sponsor = this.sponsors.find(
                (s) => s.sponsor_id === sponsorId
            );
            if (sponsor) {
                sponsor.flag = flag;
            }
        },
    },
    created() {
        this.id = localStorage.getItem("id");
        this.getData();
        this.fetchSponsors();
    },
});
