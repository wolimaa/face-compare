angular.module("app", []);
angular.module("app", ['ab-base64']).directive("selectFilesNg", function () {
    return {
        require: "ngModel",
        link: function postLink(scope, elem, attrs, ngModel) {
            elem.on("change", function (e) {
                var files = elem[0].files;
                ngModel.$setViewValue(files);
            })
        }
    }
}).controller('postserviceCtrl', function ($scope, $http, base64, $q, $timeout, $sce) {
    $scope.msg = "";
    $scope.statusval = "";
    $scope.statustext = "";
    $scope.headers = "";
    $scope.score = "";
    $scope.match = null;

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-bottom-full-width",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }

    $('#file-input').on("change", previewImages);

    function getFileBuffer(file) {
        var deferred = new $q.defer();
        var reader = new FileReader();
        reader.onloadend = function (e) {
            deferred.resolve(e.target.result);
        };
        reader.onerror = function (e) {
            deferred.reject(e.target.error);
        };
        reader.readAsDataURL(file);
        return deferred.promise;
    }

    function previewImages() {
        var $preview = $('#preview').empty();
        if (this.files) $.each(this.files, readAndPreview);

        function readAndPreview(i, file) {

            if (!/\.(jpe?g|png|gif)$/i.test(file.name)) {
                return alert(file.name + " is not an image");
            } // else...

            var reader = new FileReader();

            $(reader).on("load", function () {
                $preview.append($("<img/>", { src: this.result, height: 100 }));
            });

            reader.readAsDataURL(file);

        }

    }

    function formatTiming(millis) {
        var minutes = Math.floor(millis / 60000);
        var seconds = ((millis % 60000) / 1000).toFixed(0);
        return minutes + ":" + (seconds < 10 ? '0' : '') + seconds
    }
    $scope.postdata = function () {
        $scope.getDateTime = new Date().getTime();
        if ($scope.fileArray == undefined || $scope.fileArray.length < 2) {
            toastr.warning('Selecione duas imagens para comparação')
            return
        }

        var filesBase64 = []
        var reader = new FileReader();
        document.getElementById("json").innerHTML = JSON.stringify('Processando', undefined, 2);

        for (var i = 0, len = $scope.fileArray.length; i < len; i++) {
            var file = $scope.fileArray[i];
            getFileBuffer(file).then(function (resp) {
                filesBase64.push(resp)
            });
        }
        $timeout(function () {
            if (filesBase64.length == 2) {
                var data = {
                    image_one: filesBase64[0],
                    image_two: filesBase64[1]
                }

                var req = {
                    method: 'POST',
                    url: 'http://localhost:5000/face-compare/images',
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json',
                    },
                    data: JSON.stringify(data)
                }

                $http(req).then(function (response) {
                    if (response.data) {
                        $scope.totalTime = new Date().getTime() - $scope.getDateTime;

                        var data = {
                            response: response.data,
                            duration: formatTiming($scope.totalTime)
                        }
                        document.getElementById("json").innerHTML = JSON.stringify(data, undefined, 2);
                    }

                }).catch(function (response) {
                    /*  console.log("ERROR:", response);
                     $scope.msg = "Service not Exists";
                     $scope.statusval = response.status;
                     $scope.statustext = response.statusText;
                     $scope.headers = response.headers(); */

                    document.getElementById("json").innerHTML = JSON.stringify(response, undefined, 2);
                });

            }
        }, 2000);
    }
})