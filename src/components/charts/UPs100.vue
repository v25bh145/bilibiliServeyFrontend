<template>
    <!-- https://hub.fastgit.org/ecomfe/vue-echarts/blob/HEAD/README.zh-Hans.md -->
    <v-chart
        v-if="loading"
        :theme="theme"
        class="chart"
        :option="option"
        @click="intoEvent"
    />
</template>

<script>
import { getUPs100 } from "../../api/api";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, LineChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    DataZoomComponent,
} from "echarts/components";
import VChart from "vue-echarts";

use([
    CanvasRenderer,
    GridComponent,
    BarChart,
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    LineChart,
    DataZoomComponent,
]);

export default {
    name: "UPs100",
    props: ["theme"],
    components: {
        VChart,
    },
    data() {
        return {
            loading: false,
            fansData: [],
            rateData: [],
            option: {
                animationDelay: function (idx) {
                    // 越往后的数据延迟越大
                    return idx * 100;
                },
                title: {
                    text: "百大UP主的视频统计",
                    left: "center",
                },
                tooltip: {
                    trigger: "item",
                    formatter: "--{a}--<br>{c}",
                },
                legend: {
                    data: [
                        { name: "粉丝数", icon: "circle" },
                        { name: "总投币/总点赞", icon: "circle" },
                    ],
                    textStyle: {
                        color: "#000000",
                        fontSize: 11,
                    },
                    y: "bottom",
                    x: "center",
                    top: "30px",
                },
                dataZoom: [
                    {
                        // 这是滚动条插件  可以是Y轴 也可以是X轴
                        type: "inside",
                        start: 0,
                        end: 20,
                    },
                    {
                        start: 0,
                        end: 20,
                        handleSize: "80%",
                        handleStyle: {
                            // 图标样式
                            color: "#fff",
                            shadowBlur: 3,
                            shadowOffsetX: 4,
                            shadowOffsetY: 2,
                            transform: "rolate(90deg)",
                        },
                    },
                ],
                series: [
                    {
                        name: "粉丝数",
                        dimensions: ["UP主", "abc"],
                        type: "bar",
                        yAxisIndex: 0,
                        datasetIndex: 1,
                        data: {},
                    },
                    {
                        name: "总投币/总点赞",
                        dimensions: ["UP主", "总投币/总点赞"],
                        type: "line",
                        yAxisIndex: 1,
                        data: {},
                    },
                ],
                xAxis: {
                    type: "category",
                },
                yAxis: [
                    {
                        type: "value",
                        position: "left",
                        name: "粉丝数",
                        nameTextStyle: {
                            color: "#0",
                        },
                    },
                    {
                        type: "value",
                        position: "right",
                        name: "总投币/总点赞",
                        nameTextStyle: {
                            color: "#0",
                        },
                    },
                ],
            },
        };
    },
    methods: {
        intoEvent(params) {
            this.$emit("UPs100Click", params);
        },
        // getFansData() {
        //     return [
        //         // 第三个维度存储UP的UID
        //         ["UP主a", 1500000, 0],
        //         ["UP主b", 2200000, 1],
        //         ["UP主c", 2500000, 2],
        //         ["UP主d", 6200000, 3],
        //         ["UP主e", 620000, 4],
        //         ["UP主f", 850000, 5],
        //         ["UP主g", 4000000, 6],
        //         ["UP主h", 2500000, 7],
        //         ["UP主i", 7500000, 8],
        //         ["UP主j", 15000000, 9],
        //         ["UP主k", 11000000, 10],
        //         ["UP主l", 16000000, 11],
        //         ["UP主m", 4000000, 12],
        //         ["UP主n", 2200000, 13],
        //         ["UP主o", 1700000, 14],
        //     ];
        // },
        // getRateData() {
        //     return [
        //         // 第三个维度存储UP的UID
        //         ["UP主a", 0.85, 0],
        //         ["UP主b", 0.52, 1],
        //         ["UP主c", 0.05, 2],
        //         ["UP主d", 0.75, 3],
        //         ["UP主e", 0.72, 4],
        //         ["UP主f", 0.25, 5],
        //         ["UP主g", 0.45, 6],
        //         ["UP主h", 0.82, 7],
        //         ["UP主i", 0.125, 8],
        //         ["UP主j", 0.45, 9],
        //         ["UP主k", 0.82, 10],
        //         ["UP主l", 0.95, 11],
        //         ["UP主m", 0.45, 12],
        //         ["UP主n", 0.52, 13],
        //         ["UP主o", 0.65, 14],
        //     ];
        // },
    },
    mounted() {
        let that = this;
        that.fansData = [];
        that.rateData = [];
        let data = getUPs100();
        data.then(function (data) {
            let dataArray = data.data.message;
            for (let i = 0; i < dataArray.length; ++i) {
                that.fansData.push([
                    dataArray[i].name,
                    dataArray[i].fans,
                    dataArray[i].uid,
                ]);
                that.rateData.push([
                    dataArray[i].name,
                    dataArray[i].all_coins / dataArray[i].all_likes,
                    dataArray[i].uid,
                ]);
            }
            that.option.series[0].data = that.fansData;
            that.option.series[1].data = that.rateData;
            that.loading = true;
        });
    },
};
</script>

<style scoped>
.chart {
    top: 25px;
    position: relative;
    height: 85%;
    width: 100%;
}
</style>
