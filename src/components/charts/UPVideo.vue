<template>
    <div v-if="mainLoading" id="UPVideo-main" @click="backToChart">
        <!-- https://hub.fastgit.org/ecomfe/vue-echarts/blob/HEAD/README.zh-Hans.md -->
        <!-- 播放量 -->
        <v-chart
            :theme="theme"
            class="chart1"
            :option="playOption"
            @click="intoEvent"
        />
        <!-- 投币/点赞 -->
        <v-chart
            :theme="theme"
            class="chart2"
            :option="rateOption"
            @click="intoEvent"
        />
        <v-overlay :value="overlay">
            <v-progress-circular
                v-if="loading"
                indeterminate
                size="64"
            ></v-progress-circular>
            <videoInfo
                :class="videoAnm"
                v-if="!loading"
                :videoData="videoData"
                @intoDepartmentVideo="intoDepartmentVideo"
            />
        </v-overlay>
    </div>
</template>

<script>
import { getVideoByUser, getDepartmentByDepartmentID } from "../../api/api";
import videoInfo from "./components/videoInfo";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart, ScatterChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    VisualMapComponent,
} from "echarts/components";
import VChart from "vue-echarts";

use([
    CanvasRenderer,
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    PieChart,
    VisualMapComponent,
    ScatterChart,
]);

export default {
    props: ["UID", "UPName", "theme"],
    name: "UPVideo",
    components: {
        VChart,
        videoInfo,
    },
    data() {
        return {
            videoAnm: "",
            videoData: {},
            overlay: false,
            loading: false,
            mainLoading: false,
            rateData: [],
            playsData: [],
            dataArray: [],
            playOption: {
                title: {
                    text: this.UPName + " 的视频播放量环形统计图",
                    left: "center",
                },
                tooltip: {
                    trigger: "item",
                },
                legend: {
                    top: "5%",
                    left: "right",
                    type: "scroll",
                    width: "500px",
                    orient: "vertical",
                },
                series: [
                    {
                        name: "视频播放量统计",
                        type: "pie",
                        radius: ["40%", "70%"],
                        avoidLabelOverlap: false,
                        itemStyle: {
                            borderRadius: 10,
                            borderColor: "#fff",
                            borderWidth: 2,
                        },
                        label: {
                            show: false,
                            position: "center",
                        },
                        labelLine: {
                            show: false,
                        },
                        data: [],
                    },
                ],
            },
            rateOption: {
                animationDelay: function (idx) {
                    // 越往后的数据延迟越大
                    return idx * 100;
                },
                title: {
                    text: this.UPName + " 的视频数据分析图",
                    left: "center",
                },
                tooltip: {
                    trigger: "item",
                    axisPointer: {
                        type: "cross",
                        snap: "true",
                    },
                    showContent: "true",
                    formatter(params) {
                        return (
                            "视频: " +
                            params.value[3] +
                            "<br>点赞量: " +
                            params.value[0] +
                            "<br>投币量: " +
                            params.value[1] +
                            "<br>视频播放量: " +
                            params.value[2]
                        );
                    },
                },
                legend: {
                    top: "5%",
                    left: "right",
                    type: "scroll",
                    width: "500px",
                    orient: "vertical",
                },
                visualMap: [
                    {
                        left: "80%",
                        top: "10%",
                        dimension: 2,
                        min: 0,
                        max: 0,
                        itemWidth: 30,
                        itemHeight: 120,
                        calculable: true,
                        precision: 0.1,
                        text: ["播放量"],
                        textGap: 20,
                        inRange: {
                            symbolSize: [10, 70],
                        },
                        outOfRange: {
                            symbolSize: [10, 70],
                            color: ["rgba(255,255,255,0.4)"],
                        },
                        controller: {
                            // inRange: {
                            //     color: ["#bbb"],
                            // },
                            outOfRange: {
                                color: ["#999"],
                            },
                        },
                    },
                ],
                xAxis: {
                    type: "value",
                    name: "点赞量",
                    nameTextStyle: {
                        color: "#0",
                    },
                    axisTick: {
                        alignWithLabel: true,
                    },
                },
                yAxis: {
                    type: "value",
                    name: "投币量",
                    nameTextStyle: {
                        color: "#0",
                    },
                },
                series: [
                    {
                        type: "scatter",
                        data: [],
                    },
                ],
            },
        };
    },
    methods: {
        getVideoData(bv, cb) {
            let that = this;
            let index;
            for (let i = 0; i < that.dataArray.length; ++i) {
                if (that.dataArray[i].bv == bv) {
                    index = i;
                    break;
                }
            }
            console.log("选中 " + that.dataArray[index].bv + " " + that.dataArray[index].department_id);
            let data = getDepartmentByDepartmentID({ departmentId: that.dataArray[index].department_id });
            data.then(function (data) {
                that.tName = data.data.message[0].name;
                cb({
                    title: that.dataArray[index].name,
                    likes: that.dataArray[index].likes,
                    coins: that.dataArray[index].coins,
                    plays: that.dataArray[index].plays,
                    tName: that.tName,
                    tid: that.dataArray[index].department_id,
                    UPName: that.UPName,
                    uid: that.uid,
                    updateTime: that.dataArray[index].update_time,
                });
            });
        },
        intoEvent(params) {
            let that = this;
            // that.$emit("UPVideoClick", params);
            let bv;
            if (typeof params.data.bv == "undefined") bv = params.data[4];
            else bv = params.data.bv;
            console.log(bv);
            that.loading = true;
            that.overlay = true;
            that.getVideoData(bv, (data) => {
                that.videoAnm = "video-card-in-anm";
                that.loading = false;
                that.videoData = data;
            });
        },
        // getMaxPlays() {
        //     let rateData = this.getRateData();
        //     let maxPlays = 0;
        //     for (let i in rateData)
        //         maxPlays =
        //             maxPlays > rateData[i][2] ? maxPlays : rateData[i][2];
        //     return maxPlays;
        // },
        getPlaysData() {
            return [
                {
                    value: 106565,
                    name: "视频agsdfffgfgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a3215", bv: "fa2s4" },
                { value: 10653565, name: "视频35412", bv: "fa2s5" },
                { value: 16535, name: "视频a231", bv: "fsdv" },
                { value: 10656254, name: "视频3121", bv: "fa2s7" },
                {
                    value: 106565,
                    name: "视频1agsdfffgfgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a23215", bv: "fa2s4" },
                {
                    value: 10653565,
                    name: "视频353412",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频a2431", bv: "fsdv" },
                { value: 10656254, name: "视频31521", bv: "fa2s7" },
                {
                    value: 106565,
                    name: "视频agsdfffg2fgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a3315", bv: "fa2s4" },
                {
                    value: 10653565,
                    name: "视频3543212",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频a2341", bv: "fsdv" },
                {
                    value: 10656254,
                    name: "视频3132321",
                    bv: "fa2s7",
                },
                {
                    value: 106565,
                    name: "视频agsdf243ffgfgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a325315", bv: "fa2s4" },
                {
                    value: 10653565,
                    name: "视频342345412",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频a23231", bv: "fsdv" },
                {
                    value: 10656254,
                    name: "视频3243121",
                    bv: "fa2s7",
                },
                {
                    value: 106565,
                    name: "视频agsdf243ffgfgnggfdf",
                    bv: "fa2s3",
                },
                {
                    value: 10656,
                    name: "视频a320540215",
                    bv: "fa2s4",
                },
                {
                    value: 10653565,
                    name: "视频3455412",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频a23041", bv: "fsdv" },
                {
                    value: 10656254,
                    name: "视频3105421",
                    bv: "fa2s7",
                },
                {
                    value: 106565,
                    name: "视频agsdf04ffgfgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a322.15", bv: "fa2s4" },
                {
                    value: 10653565,
                    name: "视频35400544012",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频a205431", bv: "fsdv" },
                {
                    value: 10656254,
                    name: "视频054053121",
                    bv: "fa2s7",
                },
                {
                    value: 106565,
                    name: "视频agsdf405ffgfgnggfdf",
                    bv: "fa2s3",
                },
                {
                    value: 10656,
                    name: "视频a32140dfffgfgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a321205", bv: "fa2s4" },
                {
                    value: 10653565,
                    name: "视频354412",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频a230211", bv: "fsdv" },
                {
                    value: 10656254,
                    name: "视频311201",
                    bv: "fa2s7",
                },
                {
                    value: 106565,
                    name: "视频agsdf012ffgfgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a3210125", bv: "fa2s4" },
                {
                    value: 10653565,
                    name: "视频3025412",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频a23001", bv: "fsdv" },
                {
                    value: 10656254,
                    name: "视频322121",
                    bv: "fa2s7",
                },
                {
                    value: 106565,
                    name: "视频ags00dfffgfgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a3104215", bv: "fa2s4" },
                {
                    value: 10653565,
                    name: "视频3345412",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频a35231", bv: "fsdv" },
                {
                    value: 10656254,
                    name: "视频3123451",
                    bv: "fa2s7",
                },
                {
                    value: 106565,
                    name: "视频agsdff4fgfgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a3212.5", bv: "fa2s4" },
                {
                    value: 10653565,
                    name: "视频354.2412",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频a2312.", bv: "fsdv" },
                {
                    value: 10656254,
                    name: "视频34f121",
                    bv: "fa2s7",
                },
                {
                    value: 106565,
                    name: "视频agsdsvsddfffgfgnggfdf",
                    bv: "fa2s3",
                },
                { value: 10656, name: "视频a321fvd5", bv: "fa2s4" },
                {
                    value: 10653565,
                    name: "视频35bsb412",
                    bv: "fa2s5",
                },
                { value: 16535, name: "视频afb231", bv: "fsdv" },
                {
                    value: 10656254,
                    name: "视频3121bf",
                    bv: "fa2s7",
                },
            ];
        },
        getRateData() {
            return [
                [9, 5, 350000, "视频a", "bvfdg"],
                [7, 10, 200000, "视频b", "bvjjgthgrrbgfn"],
                [7, 15, 2000000, "视频c", "bvjkfskdds"],
            ];
        },
        intoDepartmentVideo(params) {
            this.$emit("intoDepartmentVideo", params);
        },
        backToChart() {
            let that = this;
            if (that.loading || !that.overlay) return;
            that.videoAnm = "video-card-out-anm";
            setTimeout(() => {
                that.overlay = false;
            }, 250);
        },
    },
    mounted() {
        let that = this;
        let maxPlays = 0;
        that.playsData = [];
        that.rateData = [];
        let data = getVideoByUser({ uid: that.UID });
        data.then(function (data) {
            // console.log(data.data.message);
            that.dataArray = data.data.message;
            console.log(that.dataArray);
            for (let i = 0; i < that.dataArray.length; ++i) {
                console.log("i: " + i + " all: " + that.dataArray.length);
                if(that.dataArray[i] == null) continue;
                console.log("plays: " + that.dataArray[i].plays);
                that.playsData.push({
                    value: that.dataArray[i].plays,
                    name: that.dataArray[i].name,
                    bv: that.dataArray[i].bv,
                });
                that.rateData.push([
                    that.dataArray[i].likes,
                    that.dataArray[i].coins,
                    that.dataArray[i].plays,
                    that.dataArray[i].name,
                    that.dataArray[i].bv,
                ]);
                maxPlays =
                    maxPlays > that.dataArray[i].plays
                        ? maxPlays
                        : that.dataArray[i].plays;
            }
            that.playOption.series[0].data = that.playsData;
            that.rateOption.series[0].data = that.rateData;
            that.rateOption.visualMap[0].max = maxPlays;
            that.mainLoading = true;
        });
    },
};
</script>

<style scoped>
#UPVideo-main {
    /* position: relative; */
    height: 100%;
    width: 100%;
}
.chart1 {
    /* position: relative; */
    padding-top: 20px;
    height: 45%;
    width: 100%;
}
.chart2 {
    /* position: relative; */
    padding-top: 50px;
    height: 50%;
    width: 100%;
    /* padding-right: 300px; */
}
@keyframes videoCardAnm {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
.video-card-in-anm {
    opacity: 0;
    animation-name: videoCardAnm;
    animation-fill-mode: forwards;
    animation-duration: 0.25s;
    animation-direction: normal;
    animation-timing-function: ease-in;
}
.video-card-out-anm {
    opacity: 1;
    animation-name: videoCardAnm;
    animation-fill-mode: forwards;
    animation-duration: 0.25s;
    animation-direction: reverse;
    animation-timing-function: ease-in;
}
</style>
