import { readable, Readable } from 'svelte/store';

// types/sharedState.ts
export enum AppStatus {
    IDLE = "IDLE",
    TAKING_SCREENSHOT = "TAKING_SCREENSHOT",
    UPLOADING_SCREENSHOT = "UPLOADING_SCREENSHOT",
    AI_PROCESSING = "AI_PROCESSING",
    ERROR = "ERROR",
    RECORDING = "RECORDING",
    TRANSCRIBING = "TRANSCRIBING",
    WAITING_CONNECTION = "WAITING_CONNECTION"
}

export interface SharedState {
    status: AppStatus;
    last_sync?: Date | null;
    message?: string;
    body?: string;
    prompt_profile: string;
    poll_time?: Date;
}
const defaultState: SharedState = {
    status: AppStatus.WAITING_CONNECTION,
    last_sync: null,
    message: undefined,
    body: undefined,
    prompt_profile: "",
    poll_time: new Date()
};

export const sharedStateStore: Readable<SharedState> = readable<SharedState>(defaultState, (set) => {
    const source = new EventSource('/stream'); // your SSE backend endpoint

    source.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data) as SharedState;
            set(data);
        } catch (err) {
            console.error('Failed to parse event data:', err);
        }
    };

    source.onerror = (err) => {
        console.error('SSE error:', err);
        source.close();
    };

    return () => {
        source.close(); // cleanup on unsubscribe
    };
});
