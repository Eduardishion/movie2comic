import { createStore } from 'vuex'
import { SessionStage, SessionState } from "../models/enum"

export default createStore({
  state() {
    return {
      state: SessionState.AfterCreate,
      stage: SessionStage.Create,
      sessionId: "",
      apiUrl: "http://localhost:5050"
    }
  },
  getters: {
    sessionRootUrl(state: any) {
      return `${state.apiUrl}/api/session`;
    },
    sessionUrl(state: any, getters: any) {
      return `${getters.sessionRootUrl}/${state.sessionId}`;
    },
  },
  mutations: {
    setSession(state, value) {
      state.sessionId = value;
    },
    setState(state, value) {
      state.state = value;
    },
    setStage(state, value) {
      state.stage = value;
    }
  },
  actions: {
    updateState(context) {
      const { state, getters } = context;
      if (state.sessionId) {
        fetch(`${getters.sessionUrl}/state`).then(res => res.text()).then(value => {
          context.commit("setState", parseInt(value))
        });
        fetch(`${getters.sessionUrl}/stage`).then(res => res.text()).then(value => {
          context.commit("setStage", parseInt(value))
        });
      }
    },
    autoUpdate(context) {
      setInterval(() => {
        if (context.state.sessionId != null) {
          context.dispatch("updateState");
        }
      }, 2000);
    }
  },
  modules: {
  }
})