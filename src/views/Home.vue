<template>
    <div id="home-main">
        <!-- <h1 id="total-head">B I L I B I L I 数 据 分 析</h1> -->
        <!-- <h1 id="subtitle">——数据库实践大作业</h1> -->
        <v-card id="chart-preview" shaped>
            <v-carousel v-model="model">
                <v-carousel-item v-for="chartName in charts" :key="chartName">
                    <v-sheet
                        :class="'select-sheet ' + 'select-sheet-' + chartName"
                        :color="
                            chartName == 'UPs100'
                                ? 'red lighten-3'
                                : 'purple lighten-3'
                        "
                        @click="intoChart(chartName)"
                        height="100%"
                        tile
                    >
                        <v-row
                            class="fill-height"
                            align="center"
                            justify="center"
                        >
                            <div class="text-h3 font-weight-black">
                                {{
                                    chartName == "UPs100"
                                        ? "百大UP主的视频分析"
                                        : "不同专区的视频分析"
                                }}
                            </div>
                        </v-row>
                    </v-sheet>
                </v-carousel-item>
            </v-carousel>
        </v-card>
    </div>
</template>

<script>
// import HelloWorld from "../components/HelloWorld";

export default {
    name: "Home",
    data: () => ({
        model: 0,
        charts: ["UPs100", "Departments"],
    }),
    components: {
        // HelloWorld,
    },
    methods: {
        intoChart(chartName) {
            console.log(chartName);
            this.$router.push({
                path: "/charts",
                query: { chartName: chartName },
            });
        },
    },
};
</script>
<style lang="css">
#home-main {
    background-image: url("../assets/bg_6.jpg");
    background-repeat: no-repeat;
    background-size: 100% auto;
    background-position: center 70%;
    height: 100%;
    width: 100%;
}
#total-head {
    position: relative;
    top: 50px;
    text-align: center;
    font-size: 70px;
    color: transparent;
    -webkit-text-fill-color: rgba(163, 195, 253, 0.8); /*文字的填充色*/
    /* -webkit-text-fill-color: rgba(193, 192, 255, 0.9); */
    -webkit-text-stroke: 1px rgba(0, 0, 0, 0.8);
}
#subtitle {
    position: relative;
    top: 35px;
    text-align: center;
    color: gray;
    font-size: 45px;
    -webkit-text-fill-color: rgba(163, 195, 253, 0.8); /*文字的填充色*/
    -webkit-text-stroke: 1.2px rgba(0, 0, 0, 0.8);
    left: 30%;
}
#chart-preview {
    position: relative;
    top: 235px;
    height: 40px;
    width: 40%;
    left: 50%;
    transform: translateX(-50%);
    opacity: 0.9;
}
.select-sheet:hover {
    cursor: pointer;
}
.select-sheet-Departments {
    background-image: url("../assets/Departments.png");
    background-repeat: no-repeat;
    background-size: auto 100%;
    background-position: center 0;
}
.select-sheet-UPs100 {
    background-image: url("../assets/UPs100.png");
    background-repeat: no-repeat;
    background-size: 100% 100%;
}
</style>
