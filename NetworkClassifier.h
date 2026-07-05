#pragma once
#include <cstdarg>
namespace Eloquent {
    namespace ML {
        namespace Port {
            class NetworkClassifier {
                public:
                    /**
                    * Predict class for features vector
                    */
                    int predict(float *x) {
                        if (x[0] <= 850.0) {
                            if (x[0] <= 60.0) {
                                return 1;
                            }

                            else {
                                return 0;
                            }
                        }

                        else {
                            if (x[2] <= 768.0) {
                                return 3;
                            }

                            else {
                                return 2;
                            }
                        }
                    }

                protected:
                };
            }
        }
    }