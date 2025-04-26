export interface ApiArgs {
    url: string;
    params?: object;
    data?: object;
    file?: File;
    additionalData?: object;
}

export interface ApiResult<T> {
    success: boolean;
    data?: T;
    error?: string;
}

// User API-specific data interfaces
export interface CreateUserData {
    id: string;
    name: string;
    email: string;
}

export interface GetUserData {
    id: string;
    name: string;
    email: string;
}

export interface UpdateUserData {
    id: string;
    name: string;
    email: string;
}

export interface DeleteUserData {
    message: string;
}

export interface ListUsersData {
    id: string;
    name: string;
}[]