import apiUtils from '../api';
import type { ApiResult, CreateUserData, GetUserData, UpdateUserData, DeleteUserData, ListUsersData } from './interfaces';

export const userApi = {
    async createUser(data: CreateUserData): Promise<ApiResult<CreateUserData>> {
        try {
            const response = await apiUtils.post('/users/', data);
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async getUser(userId: string): Promise<ApiResult<GetUserData>> {
        try {
            const response = await apiUtils.get(`/users/${userId}`);
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async updateUser(userId: string, data: UpdateUserData): Promise<ApiResult<UpdateUserData>> {
        try {
            const response = await apiUtils.put(`/users/${userId}`, data);
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async deleteUser(userId: string): Promise<ApiResult<DeleteUserData>> {
        try {
            const response = await apiUtils.get(`/users/${userId}`);
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async listUsers(): Promise<ApiResult<ListUsersData>> {
        try {
            const response = await apiUtils.get('/users');
            return { success: true, data: response };
        } catch (error) {
            return { success: false, error: error.message };
        }
    },

    async getMe(): Promise<ApiResult<GetUserData>> {
        try {
            const response = await apiUtils.get('/me');
            return { success: true, data: response };
        } catch (error: any) {
            return {
                success: false,
                error: error.message || 'An unknown error occurred',
                status: error.response?.status || 500
            };
        }
    },
};

export default userApi;