import { request } from "./request";

export function getUPs100(data) {
    return request({
        url: "/api/ups100",
        method: "GET",
        params: data,
    });
}
export function getDepartments(data) {
    return request({
        url: "/api/departments",
        method: "GET",
        params: data,
    });
}
export function getVideoByDepartment(data) {
    return request({
        url: "/api/getVideoByDepartment",
        method: "GET",
        params: data,
    });
}
export function getVideoByUser(data) {
    return request({
        url: "/api/getVideoByUser",
        method: "GET",
        params: data,
    });
}
export function getDepartmentByDepartmentID(data) {
    return request({
        url: "/api/getDepartmentByDepartmentID",
        method: "GET",
        params: data,
    });
}
export function getUserByUID(data) {
    return request({
        url: "/api/getUserByUID",
        method: "GET",
        params: data,
    });
}
export function getUserByBV(data) {
    return request({
        url: "/api/getUserByBV",
        method: "GET",
        params: data,
    });
}
