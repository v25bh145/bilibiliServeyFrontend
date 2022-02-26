<template>
    <!-- https://hub.fastgit.org/ecomfe/vue-echarts/blob/HEAD/README.zh-Hans.md -->
    <!-- 投币/点赞 -->
    <div v-if="mainLoading" class="DepartmentVideo-main" @click="backToChart">
        <v-chart
            :theme="theme"
            class="chart"
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
import { getVideoByDepartment, getUserByBV } from "../../api/api";
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
    props: ["TID", "TName", "theme"],
    name: "DepartmentVideo",
    components: {
        VChart,
        videoInfo,
    },
    data() {
        return {
            mainLoading: false,
            videoAnm: "",
            videoData: {},
            rateData: [],
            overlay: false,
            loading: false,
            rateOption: {
                animationDelay: function (idx) {
                    // 越往后的数据延迟越大
                    return idx * 100;
                },
                title: {
                    text: this.TName + " 的视频数据分析图(采样)",
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
                        left: "83%",
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
            let data = getUserByBV({ bv: bv });
            data.then(function (data) {
                if (data.data.message.length == 0) {
                    that.uid = -1;
                    that.UPName = "未知";
                } else {
                    that.uid = data.data.message[0].uid;
                    that.UPName = data.data.message[0].name;
                }
                cb({
                    title: that.dataArray[index].name,
                    likes: that.dataArray[index].likes,
                    coins: that.dataArray[index].coins,
                    plays: that.dataArray[index].plays,
                    tName: that.TName,
                    tid: that.dataArray[index].department_id,
                    UPName: that.UPName,
                    uid: that.uid,
                    updateTime: that.dataArray[index].update_time,
                });
            });
        },
        intoEvent(params) {
            let that = this;
            // that.$emit("DepartmentVideoClick", params);
            let bv = params.data[4];
            console.log(bv);
            that.loading = true;
            that.overlay = true;
            that.getVideoData(bv, (data) => {
                that.videoAnm = "video-card-in-anm";
                that.loading = false;
                that.videoData = data;
            });
        },
        getMaxPlays() {
            let rateData = this.getRateData();
            let maxPlays = 0;
            for (let i in rateData)
                maxPlays =
                    maxPlays > rateData[i][2] ? maxPlays : rateData[i][2];
            return maxPlays;
        },
        getRateData() {
            return [
                [9, 5, 350000, "视频a", "bvfdg"],
                [7, 10, 200000, "视频b", "bvjjgthgrrbgfn"],
                [7, 10, 2000000, "视频c", "bvjkfskdds"],
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
        that.mainLoading = false;
        let maxPlays = 0;
        that.rateData = [];
        let data = getVideoByDepartment({ tid: that.TID });
        data.then(function (data) {
            that.dataArray = data.data.message;
            for (let i = 0; i < that.dataArray.length; ++i) {
                that.rateData.push([
                    that.dataArray[i].likes,
                    that.dataArray[i].coins,
                    that.dataArray[i].plays,
                    that.dataArray[i].name,
                    that.dataArray[i].bv,
                ]);
                maxPlays =
                    maxPlays > that.rateData[i][2]
                        ? maxPlays
                        : that.rateData[i][2];
            }
            that.rateOption.series[0].data = that.rateData;
            that.rateOption.visualMap[0].max = maxPlays;
            that.mainLoading = true;
        });
    },
};
</script>

<style>
.DepartmentVideo-main {
    position: relative;
    height: 100%;
    width: 100%;
}
.chart {
    top: 25px;
    position: relative;
    height: 85%;
    width: 100%;
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
