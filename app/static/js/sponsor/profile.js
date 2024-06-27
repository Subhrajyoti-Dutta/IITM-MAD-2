new Vue({
    el: "#app",
    delimiters: ["${", "}"],
    data: {
        id: 0,
        username: "",
        sponsorData: {},
        editValues: {},
        editMode: false,
        loading: true,
    },
    computed: {
        company() {
            return this.sponsorData.Company || "";
        },
        budget() {
            return this.sponsorData.Budget || 0;
        },
    },
    methods: {
        enableEdit() {
            this.editValues = { ...this.sponsorData };
            this.editMode = true;
        },
        saveChanges() {
            this.sponsorData = { ...this.editValues };
            this.editMode = false;
            axios
                .put(`/api/sponsor_api/sponsor/${this.id}`, this.sponsorData)
                .then((response) => {
                    console.log("Data updated successfully");
                })
                .catch((error) => {
                    console.error("Error updating data:", error);
                });
        },
        cancelEdit() {
            this.editMode = false;
            this.editValues = {};
        },
    },

    created() {
        this.id = localStorage.getItem("id");
        axios
            .get(`/api/sponsor_api/sponsor/${this.id}`)
            .then((response) => {
                this.username = response.data["Username"];
                delete response.data["Username"];
                this.sponsorData = response.data;
                this.loading = false;
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                this.loading = false;
            });
    },
});
